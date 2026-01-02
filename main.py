# biblioteca necessária
from moviepy import VideoFileClip, TextClip, CompositeVideoClip


video_original = (
    VideoFileClip(r"/home/migs/Documentos/estudos/video-cut/video_origin/3continentes-96---será-que-o-natal-em-cada-continente-é-diferente.mp4")
    .subclipped(10, 70)
    .with_volume_scaled(0.8)
)


# salvar video:
resultado = CompositeVideoClip([video_original])
resultado.write_videofile(r"/home/migs/Documentos/estudos/video-cut/video_cut/natal.mp4")
