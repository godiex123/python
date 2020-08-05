import youtube_dl, sys, glob, shutil

# url como argumento
url = sys.argv[1]

# atributos para la descarga
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

# descarga del audio mp3
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

# mover a carpeta musica
file = glob.glob('*.mp3')
shutil.move(file[0], '/home/dashere/Música/')