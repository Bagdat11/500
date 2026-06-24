# main.py
import base64
import io
import os
from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image  # Суретті кішірейту үшін
from telethon import TelegramClient  # Telegram каналмен жұмыс істеу үшін
from templates import HTML_DASHBOARD, HTML_CONTROLLER

app = FastAPI()

# "static" папкасын қосу (жүктелген музыкалар осында сақталады)
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")


# 📍 СЕНІҢ ТЕЛЕГРАМ API КІЛТТЕРІҢ (Жаңағы скриншоттағы мәліметтер):
API_ID = 36888932  # Сенің App api_id
API_HASH = "a6e4e6865bccc91bac566230d6bf5298"  # Сенің App api_hash
CHANNEL_USERNAME = "@taldyk_music_box"

# Telethon клиентін құру (логинді сақтау үшін сессия файлын жасайды)
client = TelegramClient("taldyk_summer_session", API_ID, API_HASH)

live_queue = {
    "queue": [],
    "total_clicks": 0,
    "photos": [],
    "истерика": 0,
    "девочка": 0,
    "ворона": 0,
    "глаза": 0,
    "любовь": 0,
    "ню": 0,
    "пломбир": 0,
    "шашлындос": 0,
}


@app.on_event("startup")
async def startup_event():
    # Сервер іске қосылғанда Telegram-ға автоматты түрде қосылады
    await client.start()
    print("Telegram Client сәтті қосылды!")


@app.on_event("shutdown")
async def shutdown_event():
    # Сервер тоқтағанда байланысты жабады
    await client.disconnect()


@app.get("/")
def get_dashboard():
    return HTMLResponse(content=HTML_DASHBOARD)


@app.get("/phone")
def get_controller():
    return HTMLResponse(content=HTML_CONTROLLER)


# 🔍 ТЕЛЕГРАМ КАНАЛДАН МУЗЫКА ІЗДЕП, ЖҮКТЕУ РОУТЕРІ
@app.post("/search_music")
async def search_music(query: str = Form(...)):
    if not query.strip():
        return JSONResponse(
            content={"status": "error", "message": "Іздеу сөзі бос!"}
        )

    try:
        # Каналыңдағы соңғы 300 посттың ішінен аудио файлдарды іздейді
        async for message in client.iter_messages(CHANNEL_USERNAME, limit=300):
            if message.audio:
                title = message.audio.title or ""
                performer = message.audio.performer or ""
                file_name = message.file.name or ""

                # Әннің атын, авторын немесе файл атын толық тексеру
                full_text = f"{title} {performer} {file_name}".lower()

                if query.lower().strip() in full_text:
                    # Ән табылса, оның атын қауіпсіз форматқа келтіреміз
                    sanitized_name = "".join(
                        [
                            c
                            for c in file_name
                            if c.isalpha() or c.isdigit() or c in "._- "
                        ]
                    ).strip()
                    if not sanitized_name:
                        sanitized_name = f"{query.strip()}.mp3"

                    file_path = os.path.join("static", sanitized_name)

                    # Егер бұл әнді біреу бұрын жүктеген болса, қайта жүктеп уақыт құртпаймыз
                    if not os.path.exists(file_path):
                        await message.download_media(file=file_path)

                    # Әннің файл атын үлкен экран ойнатуы үшін кезекке қосамыз
                    live_queue["queue"].append(sanitized_name)
                    live_queue["total_clicks"] += 1

                    return JSONResponse(
                        content={
                            "status": "success",
                            "message": f"Ән табылды және кезекке қосылды: {sanitized_name}",
                        }
                    )

        return JSONResponse(
            content={
                "status": "error",
                "message": "Каналдан мұндай ән табылмады.",
            }
        )

    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": f"Іздеу қатесі: {str(e)}"}
        )


@app.post("/vote")
async def text_vote(title: str = Form(None), photo: UploadFile = File(None)):
    # 📸 СУРЕТТІ ҚАБЫЛДАУ ЖӘНЕ СЫҒУ (RENDER-ДІ ҚҰТҚАРУ)
    if photo:
        try:
            contents = await photo.read()
            image = Image.open(io.BytesIO(contents))
            image.thumbnail((800, 800))

            output = io.BytesIO()
            image.convert("RGB").save(output, format="JPEG", quality=40)
            compressed_contents = output.getvalue()

            encoded = base64.b64encode(compressed_contents).decode("utf-8")
            base64_url = f"data:image/jpeg;base64,{encoded}"

            live_queue["photos"].append(base64_url)

            if len(live_queue["photos"]) > 15:
                live_queue["photos"].pop(0)
        except Exception as e:
            print("Сурет өңдеу қатесі:", e)

    # 🎵 ДАЙЫН 7-8 ӘН ТАНДАУ ЛОГИКАСЫ
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

        return JSONResponse(
            content={
                "status": "success",
                "type": "song_added",
                "matched": final_key,
            }
        )

    if photo:
        return JSONResponse(content={"status": "success", "type": "photo_added"})

    return JSONResponse(
        content={"status": "error", "message": "Ештеңе жіберілеген жоқ"}
    )


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