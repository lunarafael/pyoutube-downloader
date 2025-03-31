from flask import render_template, request, send_file
from libs.downloader import VideoDownloader

def configure_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            url = request.form.get('url', '').strip()
            if not url:
                return render_template('index.html', error="Por favor, insira uma URL válida do YouTube.")

            try:
                downloader = VideoDownloader(url)
                video_buffer, filename = downloader.download_video()
                
                if not video_buffer:
                    return render_template('index.html', error="Nenhum stream de vídeo disponível.")
                
                return send_file(video_buffer, as_attachment=True, download_name=filename, mimetype="video/mp4")

            except Exception as e:
                return render_template('index.html', error=f"Erro ao processar o vídeo: {str(e)}")

        return render_template('index.html')
