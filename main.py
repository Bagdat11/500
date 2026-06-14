# main.py
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from templates import HTML_DASHBOARD, HTML_CONTROLLER

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Дауыстарды сақтайтын қарапайым локалды база
song_votes = {
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


# 📱 Телефоннан дауыс қабылдау API-і
@app.post("/vote")
def text_vote(title: str = Form(...)):
    clean_title = title.lower().trim()
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

    song_votes[final_key] += 1
    return JSONResponse(content={"status": "success", "matched": final_key})


# 🖥️ Ноутбук экраны дауыстарды алып тұруына арналған API
@app.get("/get_votes")
def get_votes():
    return JSONResponse(content=song_votes)


# 🔄 Ән ойнап біткенде дауыстарды нөлдеу API-і
@app.post("/reset_vote")
def reset_vote(song_key: str = Form(...)):
    if song_key in song_votes:
        song_votes[song_key] = 0
    return JSONResponse(content={"status": "reset_done"})


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)