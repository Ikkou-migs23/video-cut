![Video Cut](https://img.shields.io/badge/Video%20Cut-v1.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.3%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![FFmpeg](https://img.shields.io/badge/FFmpeg-required-red.svg)
# Video Cut

# Esse é um projeto de corte de vídeo simples
Este projeto permite cortar vídeos em segmentos menores com base em tempos de início e fim especificados pelo usuário. Ele é útil para quem deseja extrair partes específicas de um vídeo para edição ou compartilhamento.

## Funcionalidades
- Cortar vídeos em formatos populares (MP4 e MKV).

## Requisitos
- Python 3.9 ou superior
- Biblioteca MoviePy
- FFmpeg instalado no sistema

## Melhorias Futuras
- Suporte para mais formatos de vídeo.
- Interface gráfica para facilitar o uso.
- Velocidade de processamento aprimorada.

## Instalação
1. Clone este repositório:
    ```bash
    git clone https://github.com/seu_usuario/video-cut.git
    cd video-cut
    ```
2. Instale as dependências necessárias:
    ```bash
    pip install moviepy
    ```
3. Certifique-se de que o FFmpeg está instalado no seu sistema. Você pode baixar e instalar o FFmpeg a partir do site oficial: https://ffmpeg.org/download.html 
## Uso
1. Execute o script de corte de vídeo:
    ```bash
    python main.py
    ```
2. Siga as instruções na tela para fornecer o caminho do vídeo, o tempo de início e o tempo de fim para o corte.
3. O vídeo cortado será salvo no mesmo diretório do vídeo original com um sufixo "_cut" no nome do arquivo.
## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.
## Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.
