import socket
import struct
import threading
import os
from datetime import datetime
from tkinter import Tk, Label
from PIL import Image, ImageTk

# Passo 1 --- Configurações ---
HOST = '0.0.0.0'  # Escuta em todas as interfaces de rede 
PORT = 5001       # Porta para escutar 
SAVE_DIR = "data" # Diretório para salvar as imagens recebidas

# --- Classe da Aplicação GUI com Tkinter ---
class ImageServerApp:
    """ Esta classe gerencia a janela que exibe a imagem. """
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Servidor - Última Foto Recebida")
        self.root.geometry("640x520")

        # Label que mostrará o status ou a imagem
        self.label = Label(self.root, text="Aguardando primeira foto...", font=("Helvetica", 16))
        self.label.pack(expand=True)
        
        # Garante que o diretório de salvamento exista
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)

    def update_image(self, image_path):
        """ Carrega e exibe a imagem mais recente na janela. """
        try:
            img = Image.open(image_path)
            img.thumbnail((640, 480)) # Redimensiona para caber na janela
            
            # Converte a imagem para um formato que o Tkinter pode exibir
            self.photo_img = ImageTk.PhotoImage(img)

            # Atualiza o label para mostrar a nova imagem
            self.label.config(image=self.photo_img, text="")
            print(f"Janela atualizada com a imagem: {image_path}")

        except Exception as e:
            error_msg = f"Erro ao exibir imagem: {e}"
            self.label.config(text=error_msg)
            print(error_msg)

# --- Lógica do Servidor de Sockets ---
def handle_client(conn, addr, app_gui):
    """ Função executada em uma thread para cada cliente conectado. """
    print(f"Conectado por {addr}")
    try:
        # Passo 3.1: Receber o tamanho da imagem (4 bytes) de forma robusta
        packed_size = b''
        while len(packed_size) < 4:
            # Pede os bytes que faltam para completar os 4
            chunk = conn.recv(4 - len(packed_size))
            if not chunk:
                # Se não receber nada, o cliente desconectou
                print(f"Cliente {addr} desconectou prematuramente.")
                return # Termina a função para esta thread
            packed_size += chunk

        # Se chegamos aqui, temos os 4 bytes
        img_size = struct.unpack('>I', packed_size)[0]
        print(f"Recebendo imagem de {img_size} bytes de {addr}")

        # Passo 3.2: Receber os dados da imagem em partes até o tamanho total
        img_data = b''
        while len(img_data) < img_size:
            chunk = conn.recv(4096)
            if not chunk:
                break
            img_data += chunk
        
        # Verifica se a imagem foi recebida por completo
        if len(img_data) != img_size:
            print(f"Erro: Recebidos {len(img_data)} de {img_size} bytes. Imagem incompleta.")
            return

        # Passo 3.3: Salvar a imagem em disco
        now = datetime.now()
        date_dir = now.strftime("%Y-%m-%d")
        full_dir_path = os.path.join(SAVE_DIR, date_dir)
        
        if not os.path.exists(full_dir_path):
            os.makedirs(full_dir_path)

        filename = now.strftime("%H%M%S") + ".jpg"
        filepath = os.path.join(full_dir_path, filename)

        with open(filepath, 'wb') as img_file:
            img_file.write(img_data)
        
        print(f"Imagem salva em: {filepath} ({img_size} bytes)")

        # Passo 4: Atualizar a GUI na thread principal
        app_gui.root.after(0, app_gui.update_image, filepath)

    except Exception as e:
        print(f"Erro ao lidar com o cliente {addr}: {e}")
    finally:
        conn.close()
        print(f"Conexão com {addr} fechada.")

def start_server(app_gui):
    """ Inicia o servidor TCP para ouvir por conexões. """
    # Passo 2: Criação, vínculo e escuta do socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor ouvindo em {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            # Inicia uma nova thread para cada cliente para não bloquear a GUI
            client_thread = threading.Thread(target=handle_client, args=(conn, addr, app_gui))
            client_thread.daemon = True
            client_thread.start()

# --- Bloco Principal de Execução ---
if __name__ == "__main__":
    # Inicia a interface gráfica
    root = Tk()
    app = ImageServerApp(root)

    # Inicia o servidor de sockets em uma thread separada
    server_thread = threading.Thread(target=start_server, args=(app,))
    server_thread.daemon = True
    server_thread.start()

    # Inicia o loop principal da GUI (isso deve ser a última chamada)
    root.mainloop()