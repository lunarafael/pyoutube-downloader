from pytubefix import YouTube

class VideoDownloader:
    def __init__(self, url):
        self.url = url.split("&")[0] if "youtube.com" in url and "&" in url else url
        self.yt = YouTube(self.url)

    def get_video_info(self):
        streams = self.yt.streams
        
        video_streams = streams.filter(file_extension="mp4", type="video")
        
        resolutions = {}
        for stream in video_streams:
            res = stream.resolution
            if not res:
                continue

            if res in resolutions:
                current = resolutions[res]
                if stream.is_progressive and not current.is_progressive:
                    resolutions[res] = stream
                elif (stream.is_progressive == current.is_progressive) and (stream.fps > current.fps):
                    resolutions[res] = stream
            else:
                resolutions[res] = stream

        video_options = []
        for res, stream in resolutions.items():
            video_options.append({
                "itag": stream.itag,
                "resolution": f"{res} ({stream.fps} FPS)",
                "type": "video",
                "audio": "Sim" if stream.is_progressive else "Não"
            })

        video_options.sort(key=lambda x: int(x["resolution"].split("p")[0]), reverse=True)

        audio_streams = streams.filter(only_audio=True, file_extension="mp4").order_by("abr").desc()
        audio_options = []

        for stream in audio_streams[:3]:
            audio_options.append({
                "itag": stream.itag,
                "resolution": f"{stream.abr} Áudio",
                "codec": stream.audio_codec,
                "type": "audio"
            })
        
        return {
            "title": self.yt.title,
            "thumbnail": self.yt.thumbnail_url,
            "options": video_options + audio_options
        }

    def download_by_itag(self, itag):
        stream = self.yt.streams.get_by_itag(itag)

        if not stream:
            return None, None

        from io import BytesIO
        buffer = BytesIO()
        stream.stream_to_buffer(buffer)
        buffer.seek(0)

        return buffer, f"{self.yt.title}.mp4"