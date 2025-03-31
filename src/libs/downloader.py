from pytubefix import YouTube
from io import BytesIO

class VideoDownloader:
    def __init__(self, url):
        # Remove parâmetros extras da URL
        self.url = url.split("&")[0] if "youtube.com" in url and "&" in url else url

    def download_video(self):
        yt = YouTube(self.url)
        stream = yt.streams.get_highest_resolution()

        if not stream:
            return None, None

        # Baixa o vídeo para a memória
        buffer = BytesIO()
        stream.stream_to_buffer(buffer)
        buffer.seek(0)

        return buffer, f"{yt.title}.mp4"
