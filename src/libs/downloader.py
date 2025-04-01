from pytubefix import YouTube
from pytubefix.request import _execute_request
from io import BytesIO
import os
from moviepy.editor import VideoFileClip, AudioFileClip
import logging

logging.basicConfig(level=logging.INFO)

default_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'accept-language': 'en-US,en;q=0.9',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'referer': 'https://www.youtube.com/',
    'origin': 'https://www.youtube.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'dnt': '1',
}

original_execute_request = _execute_request

def custom_execute_request(
    url,
    method=None,
    headers=None,
    data=None,
    timeout=None
):
    if headers is None:
        headers = {}
    headers.update(default_headers)
    return original_execute_request(url, method, headers, data, timeout)

_execute_request = custom_execute_request

class VideoDownloader:
    def __init__(self, url):
        try:
            self.url = url.split("&")[0] if "youtube.com" in url and "&" in url else url
            self.yt = YouTube(
                self.url,
                'ANDROID'
            )
            self.yt._vid_info
        except Exception as e:
            logging.error(f"Error initializing YouTube object: {str(e)}")
            raise

    def get_video_info(self):
        try:
            streams = self.yt.streams
            
            video_streams = streams.filter(file_extension="mp4", type="video")
            
            resolutions = {}
            for stream in video_streams:
                res = stream.resolution
                if not res:
                    continue

                if res in resolutions:
                    current = resolutions[res]
                    if (stream.is_progressive and not current.is_progressive) or \
                    (stream.is_progressive == current.is_progressive and stream.fps > current.fps):
                        resolutions[res] = stream
                else:
                    resolutions[res] = stream

            video_options = []
            for res, stream in resolutions.items():
                video_options.append({
                    "itag": stream.itag,
                    "resolution": f"{res} ({stream.fps} FPS)",
                    "type": "video",
                    "audio": "Sim" if stream.is_progressive else "Não",
                    "progressive": stream.is_progressive
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
        except Exception as e:
            logging.error(f"Error getting video info: {str(e)}")
            raise

    def download_by_itag(self, itag):
        stream = self.yt.streams.get_by_itag(itag)

        if not stream:
            return None, None

        if stream.is_progressive:
            buffer = BytesIO()
            stream.stream_to_buffer(buffer)
            buffer.seek(0)
            return buffer, f"{self.yt.title}.mp4"
        
        else:
            video_buffer = BytesIO()
            stream.stream_to_buffer(video_buffer)
            video_buffer.seek(0)

            audio_stream = self.yt.streams.filter(only_audio=True, file_extension="mp4").order_by("abr").desc().first()
            audio_buffer = BytesIO()
            audio_stream.stream_to_buffer(audio_buffer)
            audio_buffer.seek(0)

            temp_video = "temp_video.mp4"
            temp_audio = "temp_audio.mp4"
            temp_output = "output_final.mp4"

            with open(temp_video, "wb") as f:
                f.write(video_buffer.getbuffer())
            
            with open(temp_audio, "wb") as f:
                f.write(audio_buffer.getbuffer())

            video_clip = VideoFileClip(temp_video)
            audio_clip = AudioFileClip(temp_audio)
            
            final_clip = video_clip.set_audio(audio_clip)
            final_clip.write_videofile(
                temp_output,
                codec="libx264",
                audio_codec="aac",
                threads=4,
                preset="ultrafast"
            )

            with open(temp_output, "rb") as f:
                final_buffer = BytesIO(f.read())
            
            final_buffer.seek(0)

            video_clip.close()
            audio_clip.close()
            if os.path.exists(temp_video):
                os.remove(temp_video)
            if os.path.exists(temp_audio):
                os.remove(temp_audio)
            if os.path.exists(temp_output):
                os.remove(temp_output)

            return final_buffer, f"{self.yt.title}.mp4"