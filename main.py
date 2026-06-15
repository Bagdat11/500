# main.py
from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import base64
from typing import Optional
from templates import HTML_DASHBOARD, HTML_CONTROLLER

app = FastAPI()

# Статикалық файлдар папкасын тексеру
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Ортақ мәліметтер базасы
live_queue = {
    "queue": [],
    "total_clicks": 0,
    "photos": [],
    "истерика": 0, "девочка": 0, "ворона": 0, "глаза": 0, "любовь": 0, "ню": 0, "пломбир": 0, "шашлындос": 0,
    "bass": 0,  # Бастапқы басс
    "volume": 1.0  # Бастапқы дыбыс деңгейі
}


@app.get("/")
def get_dashboard():
    return HTMLResponse(content=HTML_DASHBOARD)


@app.get("/phone")
def get_controller():
    return HTMLResponse(content=HTML_CONTROLLER)


# 🎛️ МИКШЕРДІ ЖАҢАРТУ API (Жеңілдетілген нұсқасы)
@app.post("/update_mixer")
async def update_mixer(data: dict):
    live_queue["bass"] = int(data.get("bass", 0))
    live_queue["volume"] = float(data.get("volume", 1.0))
    return JSONResponse(content={"status": "success"})


# 📱 ДАУЫС БЕРУ ЖӘНЕ ФОТО ЖІБЕРУ API
@app.post("/vote")
async def text_vote(title: Optional[str] = Form(None), photo: Optional[UploadFile] = File(None)):
    if photo:
        try:
            contents = await photo.read()
            encoded = base64.b64encode(contents).decode("utf-8")
            mime_type = photo.content_type or "image/jpeg"
            base64_url = f"data:{mime_type};base64,{encoded}"
            live_queue["photos"].append(base64_url)
        except Exception as e:
            print("Сурет өңдеу қатесі:", e)

    if title and title.strip() != "":
        clean_title = title.lower().strip()
        final_key = "шашлындос"

        if "истерика" in clean_title or "джиос" in clean_title:
            final_key = "истерика"
        elif "девочка" in clean_title or "ханза" in clean_title:
            final_key = "девочка"
        elif "ворона" in clean_title or "кэнни" in clean_title:
            final_key = "ворона"
        elif "глаза" in clean_title or "твои" in clean_title:
            final_key = "глаза"
        elif "любовь" in clean_title or "слова" in clean_title:
            final_key = "любовь"
        elif "ню" in clean_title or "получается" in clean_title:
            final_key = "ню"
        elif "пломбир" in clean_title or "раса" in clean_title:
            final_key = "пломбир"
        elif "шашлы" in clean_title or "хлеб" in clean_title:
            final_key = "шашлындос"

        live_queue["queue"].append(final_key)
        live_queue["total_clicks"] += 1
        live_queue[final_key] += 1

        return JSONResponse(content={"status": "success", "type": "song_added", "matched": final_key})

    if photo:
        return JSONResponse(content={"status": "success", "type": "photo_added"})

    return JSONResponse(content={"status": "error", "message": "Ештеңе жіберілмеді"})


@app.get("/get_votes")
def get_votes():
    return JSONResponse(content=live_queue)


@app.get("/pop_queue")
def pop_queue():
    if len(live_queue["queue"]) > 0:
        popped_song = live_queue["queue"].pop(0)
        return JSONResponse(content={"status": "popped", "song": popped_song})
    return JSONResponse(content={"status": "empty"})


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)