# main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
import os
from templates import HTML_DASHBOARD, HTML_CONTROLLER

app = FastAPI()

# Папкадағы музыкаларды браузерге бұғаттаусыз беру үшін static-ті тіркейміз
app.mount("/static", StaticFiles(directory="static"), name="static")

connected_clients = set()


@app.get("/")
def get_dashboard():
    return HTMLResponse(content=HTML_DASHBOARD)


@app.get("/phone")
def get_controller():
    return HTMLResponse(content=HTML_CONTROLLER)


@app.websocket("/ws")
async def websocket_endpoint(websocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message.get("type") == "song_vote":
                # Келген хабарламаны барлық белсенді терезелерге (Экранға) жібереміз
                for client in connected_clients:
                    try:
                        await client.send_text(json.dumps({
                            "type": "song_vote",
                            "title": message.get("title")
                        }))
                    except:
                        pass
    except Exception as e:
        print(f"WebSocket үзілісі: {e}")
    finally:
        try:
            connected_clients.remove(websocket)
        except:
            pass


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)