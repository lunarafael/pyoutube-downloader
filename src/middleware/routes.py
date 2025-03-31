from flask import render_template, request, send_file, jsonify
from libs.downloader import VideoDownloader

def configure_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    def index():
        return render_template('index.html')

    @app.route('/get_video_info', methods=['POST'])
    def get_video_info():
        url = request.json.get("url", "").strip()
        if not url:
            return jsonify({"error": "Por favor, insira uma URL válida do YouTube."})

        try:
            downloader = VideoDownloader(url)
            video_info = downloader.get_video_info()
            return jsonify(video_info)
        except Exception as e:
            return jsonify({"error": f"Erro ao processar o vídeo: {str(e)}"})

    @app.route('/download/<itag>', methods=['GET'])
    def download(itag):
        url = request.args.get("url", "").strip()
        if not url:
            return "Erro: URL inválida"

        try:
            downloader = VideoDownloader(url)
            video_buffer, filename = downloader.download_by_itag(itag)

            if not video_buffer:
                return "Erro: Nenhum stream disponível."

            return send_file(video_buffer, as_attachment=True, download_name=filename, mimetype="video/mp4")

        except Exception as e:
            return f"Erro ao processar o vídeo: {str(e)}"