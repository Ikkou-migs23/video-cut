# biblioteca necessária
from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import time
import os 

# variavel contendo o arquivo original
caminho_video_original = r"/home/migs/Documentos/estudos/video-cut/video_origin/3continentes-96---será-que-o-natal-em-cada-continente-é-diferente.mp4"
caminho_video_corte = r"/home/migs/Documentos/estudos/video-cut/video_cut"
os.makedirs(caminho_video_corte, exist_ok=True)


# constantes
video = VideoFileClip(caminho_video_original)
duracao_total = video.duration
duracao_corte = 60
numero_cortes = int(duracao_total // duracao_corte)

print(f"Iniciando os {numero_cortes} cortes")

# loop para a produção dos cortes:
for i in range(numero_cortes):
    inicio = i * duracao_corte
    fim = inicio + duracao_corte

    print(f"Corte {i+1}/{numero_cortes}")
          
    # carregar o video original dentro do loop a cada corte:
    video_original = VideoFileClip(caminho_video_original)
    
    # criar os cortes
    corte = video_original.subclipped(inicio, fim)

    # salvar
    corte.write_videofile(os.path.join(caminho_video_corte, f"natal_{i+1:03d}.mp4"))

    # Liberar memória
    corte.close()
    video_original.close()

    # Esperar 2 segundos
    if i < numero_cortes - 1:  # Não esperar após o último
        print("Aguardando 2 segundos...")
        time.sleep(2)
    print("Cortes realizados")

# Ultima etapa, pegar o ultimo corte (podemos chamar de sobra)
tempo_total_cortes = duracao_corte * numero_cortes
# loop para pegar o ultimo pedaço do video:
for i in range(1):
    inicio = tempo_total_cortes
    fim = duracao_total
    # carregar o video original dentro do loop a cada corte:
    video_original = VideoFileClip(caminho_video_original)
    
    # criar os cortes
    corte = video_original.subclipped(inicio, fim)

    # salvar
    corte.write_videofile(os.path.join(caminho_video_corte, "natal_57.mp4"))

    # Liberar memória
    corte.close()
    video_original.close()

    # Esperar 2 segundos
    if i < numero_cortes - 1:  # Não esperar após o último
        print("Aguardando 2 segundos...")
        time.sleep(2)
    print("Corte da sobra realizada")

print("Todos os cortes concluídos!")