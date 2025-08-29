import socket
import os
import struct
import time
import random
import glob

# --- Configurações do Teste ---
HOST = '127.0.0.1'
PORT = 5001
# Pasta onde estão as imagens que serão usadas no teste
TEST_IMAGES_DIR = 'imagens_de_teste' 
# Quantas imagens aleatórias queremos enviar no total
NUMBER_OF_IMAGES_TO_SEND = 29

MIN_INTERVAL = 5
MAX_INTERVAL = 12


def find_available_images(directory):
    """ Encontra todos os arquivos de imagem (.jpg, .jpeg, .png) em um diretório. """
    patterns = ('*.jpg', '*.jpeg', '*.png')
    image_paths = []
    for pattern in patterns:
        # O os.path.join garante que o caminho seja construído corretamente
        search_path = os.path.join(directory, pattern)
        image_paths.extend(glob.glob(search_path))
    return image_paths

def send_image(image_path):
    """ Conecta ao servidor e envia uma única imagem. """
    image_size = os.path.getsize(image_path)
    
    print(f"Iniciando envio de '{os.path.basename(image_path)}' ({image_size} bytes)...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            
            # Protocolo: Envia o tamanho (4 bytes) e depois os dados da imagem
            packed_size = struct.pack('>I', image_size)
            s.sendall(packed_size)
            
            with open(image_path, 'rb') as img_file:
                s.sendall(img_file.read())
            
            print("Envio client 2 concluído com sucesso.")
            return True

        except ConnectionRefusedError:
            print("ERRO: A conexão foi recusada. O servidor está rodando?")
        except Exception as e:
            print(f"ERRO durante o envio: {e}")
    return False

if __name__ == "__main__":
    print("--- INICIANDO TESTE DE ESTRESSE DO SERVIDOR COM CLIENTE 2 ---")
    
    # 1. Encontra as imagens na pasta de teste
    available_images = find_available_images(TEST_IMAGES_DIR)
    
    if not available_images:
        print(f"ERRO: Nenhuma imagem encontrada na pasta '{TEST_IMAGES_DIR}'.")
        print("Por favor, adicione arquivos .jpg ou .png para iniciar o teste.")
    else:
        print(f"{len(available_images)} imagens encontradas. Iniciando o envio de {NUMBER_OF_IMAGES_TO_SEND} imagens aleatórias.")
        print("-" * 50)

        # 2. Loop para enviar várias imagens
        for i in range(NUMBER_OF_IMAGES_TO_SEND):
            # Escolhe uma imagem aleatória da lista
            random_image = random.choice(available_images)
            
            print(f"Teste {i + 1}/{NUMBER_OF_IMAGES_TO_SEND}:")
            send_image(random_image)
            
            # Pausa por um tempo aleatório antes do próximo envio
            if i < NUMBER_OF_IMAGES_TO_SEND - 1:
                sleep_time = random.uniform(MIN_INTERVAL, MAX_INTERVAL)
                print(f"\nAguardando por {sleep_time:.1f} segundos...")
                time.sleep(sleep_time)
                print("-" * 50)
        
        print("\n--- TESTE DE ESTRESSE FINALIZADO ---")