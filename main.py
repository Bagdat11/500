# main.py
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from templates import HTML_DASHBOARD, HTML_CONTROLLER

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Әндердің кезегін (List) сақтайтын жаңа база
live_queue = {
    "queue": [],  # Телефоннан келген әндер осы тізімге ретімен жиналады
    "total_clicks": 0,
    "истерика": 0,
    "девочка": 0,
    "ворона": 0,
    "глаза": 0,
    "любовь": 0,
    "ню": 0,
    "пломбир": 0,
    "шашлындос": 0
}


@app.get("/")
def get_dashboard():
    return HTMLResponse(content=HTML_DASHBOARD)


@app.get("/phone")
def get_controller():
    return HTMLResponse(content=HTML_CONTROLLER)


# 📱 Телефоннан ән келгенде оны тізімнің соңына қосамыз (Резерв)
@app.post("/vote")
def text_vote(title: str = Form(...)):
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

    # Кезекке (резервке) қосу
    live_queue["queue"].append(final_key)
    live_queue["total_clicks"] += 1
    live_queue[final_key] += 1

    return JSONResponse(content={"status": "success", "matched": final_key})


# 🖥️ Ноутбукке кезекті көрсетіп тұру
@app.get("/get_votes")
def get_votes():
    return JSONResponse(content=live_queue)


# ⏭️ Ноутбуктен немесе автоматты түрде келесі әнге көшкенде тізімнен бірінші әнді алып тастау
@app.post("/pop_queue")
def pop_queue():
    if len(live_queue["queue"]) > 0:
        popped_song = live_queue["queue"].pop(0)  # Бірінші тұрған әнді суырып аламыз
        return JSONResponse(content={"status": "popped", "song": popped_song})
    return JSONResponse(content={"status": "empty"})


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)