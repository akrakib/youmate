from flask import Flask, request, send_file
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

DOWNLOAD_FOLDER = "downloads"
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
        "quiet": False
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            filename = ydl.prepare_filename(info)
            full_path = os.path.join(DOWNLOAD_FOLDER, os.path.basename(filename))

        return send_file(full_path, as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)