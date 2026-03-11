from fastapi import FastAPI, HTTPException
import yt_dlp
import uvicorn

app = FastAPI()

@app.get("/get_download_url")
def get_url(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="No URL provided")

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "status": "success",
                "title": info.get('title', 'video'),
                "url": info.get('url'),
                "thumbnail": info.get('thumbnail'),
                "ext": info.get('ext', 'mp4')
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)