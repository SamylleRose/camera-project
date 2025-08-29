# Servidor Python para Recebimento de Imagens

Este projeto é um servidor TCP construído em Python, projetado para receber arquivos de imagem de um cliente, salvá-los em disco e exibir a imagem mais recente em uma interface gráfica.

## Funcionalidades Principais

  * **Recepção de Imagens:** Ouve por conexões TCP em uma porta configurada (`5001` por padrão) e recebe dados de imagem.
  * **Armazenamento Organizado:** Salva as imagens recebidas em um diretório `data/`, criando subpastas por data (`AAAA-MM-DD`) para melhor organização.
  * **Visualização em Tempo Real:** Uma interface gráfica simples exibe a última imagem recebida, atualizando-se automaticamente a cada novo envio.
  * **Suporte a Múltiplos Clientes:** Utiliza threading para lidar com cada conexão de cliente, garantindo que o servidor permaneça responsivo.

## Tecnologias Utilizadas

  * **Python 3**
  * **Tkinter** para a interface gráfica.
  * **Pillow (PIL)** para manipulação e exibição de imagens.

## Pré-requisitos

Para executar o servidor, você precisa ter o Python 3 instalado, além da biblioteca Pillow.

```bash
pip install Pillow
```

## Como Executar

1.  Clone ou faça o download deste repositório.
2.  Navegue até a pasta do projeto pelo terminal.
3.  Execute o script do servidor:
    ```bash
    python server.py
    ```
4.  O terminal indicará que o servidor está ativo, e uma janela gráfica aparecerá, pronta para receber a primeira imagem.

## Protocolo de Comunicação

O cliente deve seguir um protocolo simples para enviar a imagem:

1.  **Cabeçalho de Tamanho:** Enviar um número inteiro de **4 bytes** (big-endian) que representa o tamanho exato da imagem em bytes.
2.  **Dados da Imagem:** Enviar os dados brutos da imagem (em formato JPEG ou PNG) imediatamente após o cabeçalho.

## Estrutura de Arquivos

```
.
├── server.py             # Script principal do servidor
├── data/                   # Diretório criado automaticamente para salvar as imagens
│   └── 2025-08-25/         # Subpasta de exemplo, criada por data
│       └── 132449.jpg      # Imagem de exemplo, nomeada pela hora
└── README.md             # Este arquivo
```