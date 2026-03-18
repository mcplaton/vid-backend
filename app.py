from flask import Flask, request, send_file
import yt_dlp
import os
import glob
import threading
import time

app = Flask(__name__)

def cleanup_old_files():
    for f in glob.glob("temp_vidgo_*"):
        try:
            if os.path.getmtime(f) < time.time() - 600:
                os.remove(f)
        except:
            pass

@app.route('/')
def home():
    return "VidGo API is Running on Render 🚀"

@app.route('/download')
def download_media():
    url = request.args.get('url')
    is_audio = request.args.get('type') == 'audio'

    if not url:
        return {"error": "No URL provided"}, 400

    threading.Thread(target=cleanup_old_files).start()

    opts = {
        'format': 'm4a/bestaudio/best' if is_audio else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'temp_vidgo_%(id)s_%(ext)s',
        'quiet': True,
        'noplaylist': True,
    }

    try:
        print(f"🚀 Downloading: {url} | Audio Only: {is_audio}")
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        print(f"✅ Success! Sending file...")
        return send_file(filename, as_attachment=True)
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": str(e)}, 500

# ما نحتاج نكتب app.run هنا لأن Render راح يشغله عن طريق gunicorn
