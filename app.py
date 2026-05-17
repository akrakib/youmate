from flask import Flask, request, send_file
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

# Render-safe temp folder
DOWNLOAD_FOLDER = "/tmp"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "Server is running"

@app.route("/download")
def download():
    url = request.args.get("url")

    if not url:
        return "No URL provided", 400

    ydl_opts = {
        "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
        "format": "best",
        "noplaylist": True,
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        # safety check
        if not os.path.exists(file_path):
            return "Download failed / file not found", 500

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}", 500


# ✅ REQUIRED FOR RENDER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=False)
