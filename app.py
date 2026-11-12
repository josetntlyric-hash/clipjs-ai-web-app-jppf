from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import os
import uuid
app = Flask(__name__)
CORS(app)
@app.route('/')
def inicio():
    return send_from_directory('.', 'index.html')
@app.route('/cortar', methods=['POST'])
def cortar():
    link = request.json.get('link')
    if not link:
        return jsonify({"error": "Pega un link"}), 400
    id_unico = str(uuid.uuid4())[:8]
    video = f"video_{id_unico}.mp4"
    clip = f"clip_{id_unico}.mp4"
    try:
        subprocess.run(["yt-dlp", "-f", "mp4", "-o", video, link], timeout=120)
        if not os.path.exists(video):
            return jsonify({"error": "YouTube no dejo descargar"}), 400
        subprocess.run(["ffmpeg", "-y", "-i", video, "-t", "30", "-c:v", "libx264", "-c:a", "aac", clip], timeout=120)
        if os.path.exists(video):
            os.remove(video)
        return jsonify({"ok": True, "clip_gratis": f"/ver/{clip}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/ver/<nombre>')
def ver(nombre):
    return send_file(nombre, mimetype='video/mp4')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
