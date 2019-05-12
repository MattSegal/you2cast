import youtube_dl

YOUTUBE_OPTS = {
    'outtmpl': '%(id)s.%(ext)s',
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

def download_youtube(url, download=True):
    with youtube_dl.YoutubeDL(YOUTUBE_OPTS) as ydl:
        result = ydl.extract_info(url, download=download)
    
    return result