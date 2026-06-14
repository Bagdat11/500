# main.py
from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import base64
from templates import HTML_DASHBOARD, HTML_CONTROLLER

app = FastAPI()

# mp3 файлдар тұрған статикалық папканы жалғау
app.mount("/static", StaticFiles(directory="static"), name="static")

# Кезек пен фотоларды жедел жадында (RAM) қауіпсіз сақтау базасы
live_queue = {
    "queue": [],  # Телефоннан келген әндер осы тізімге ретімен жиналады
    "total_clicks": 0,
    "photos": [],  # Суреттер осы жерге Base64 форматында жиналады
    "истерика": 0, "девочка": 0, "ворона": 0, "глаза": 0, "любовь": 0, "ню": 0, "пломбир": 0, "шашлындос": 0
}


@app.get("/")
def get_dashboard():
    return HTMLResponse(content=HTML_DASHBOARD)


@app.get("/phone")
def get_controller():
    return HTMLResponse(content=HTML_CONTROLLER)


# 📱 Телефоннан ән мен суретті бір уақытта қабылдау API-і
@app.post("/vote")
async def text_vote(title: str = Form(...), photo: UploadFile = File(None)):
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

    # Фотоны дискке жазбай, лезде Base64 мәтініне айналдырып, RAM-ға сақтаймыз
    if photo:
        try:
            contents = await photo.read()
            encoded = base64.b64encode(contents).decode("utf-8")
            mime_type = photo.content_type or "image/jpeg"
            base64_url = f"data:{mime_type};base64,{encoded}"
            live_queue["photos"].append(base64_url)
        except Exception as e:
            print("Сурет өңдеу қатесі:", e)

    live_queue["queue"].append(final_key)
    live_queue["total_clicks"] += 1
    live_queue[final_key] += 1

    return JSONResponse(content={"status": "success", "matched": final_key})


# 🖥️ Ноутбук экранына бүкіл кезекті және фотоларды көрсетіп тұру
@app.get("/get_votes")
def get_votes():
    return JSONResponse(content=live_queue)


# ⏭️ Кезектегі бірінші әнді суырып алу (GET арқылы тұрақты жұмыс істейді)
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