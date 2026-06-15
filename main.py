# main.py
from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import base64
import io
from PIL import Image  # Суретті кішірейту үшін
from templates import HTML_DASHBOARD, HTML_CONTROLLER

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

live_queue = {
    "queue": [],
    "total_clicks": 0,
    "photos": [],
    "истерика": 0, "девочка": 0, "ворона": 0, "глаза": 0, "любовь": 0, "ню": 0, "пломбир": 0, "шашлындос": 0
}


@app.get("/")
def get_dashboard():
    return HTMLResponse(content=HTML_DASHBOARD)


@app.get("/phone")
def get_controller():
    return HTMLResponse(content=HTML_CONTROLLER)


@app.post("/vote")
async def text_vote(title: str = Form(None), photo: UploadFile = File(None)):
    # 📸 СУРЕТТІ ҚАБЫЛДАУ ЖӘНЕ ОНЫ СЕКУНДТA СЫҒУ (RENDER-ДІ ҚҰТҚАРУ)
    if photo:
        try:
            contents = await photo.read()
            image = Image.open(io.BytesIO(contents))

            # Егер сурет өте үлкен болса, оның өлшемін азайтамыз
            image.thumbnail((800, 800))

            # Суретті сапасын түсіріп, өте жеңіл JPEG қылып RAM-ға сақтаймыз
            output = io.BytesIO()
            image.convert("RGB").save(output, format="JPEG", quality=40)  # Сапасы 40% (Өте жеңіл)
            compressed_contents = output.getvalue()

            encoded = base64.b64encode(compressed_contents).decode("utf-8")
            base64_url = f"data:image/jpeg;base64,{encoded}"

            live_queue["photos"].append(base64_url)

            # Егер фото жиналып кетсе, ескілерін өшіріп, RAM-ды тазалап отырамыз
            if len(live_queue["photos"]) > 15:
                live_queue["photos"].pop(0)

        except Exception as e:
            print("Сурет өңдеу қатесі:", e)

    # 🎵 ӘН ТАНДАУ ЛОГИКАСЫ (Сенің таза кодың)
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

    return JSONResponse(content={"status": "error", "message": "Ештеңе жіберілеген жоқ"})


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