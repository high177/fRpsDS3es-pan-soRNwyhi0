from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from sheets import fetch_data, get_cached_data
import uvicorn
import threading
import time

app = FastAPI()

@app.get("/")
def index():
    return {"status": "ok", "message": "Espanso API is running."}

@app.get("/trigger/{trigger}", response_class=PlainTextResponse)
def get_trigger(trigger: str):
    data = get_cached_data()
    trigger_full = f":{trigger}".lower()
    for row in data:
        if row.get("trigger", "").lower() == trigger_full:
            return row.get("output", "")
    return "❌ Trigger tidak ditemukan"

@app.get("/refresh")
def refresh_data():
    fetch_data()
    return {"status": "refreshed"}

# Jalankan lokal (opsional)
if __name__ == "__main__":
    fetch_data()
    threading.Thread(target=auto_refresh, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=8000)

def auto_refresh():
    while True:
        print("🔁 Auto-refreshing data from Google Sheets...")
        fetch_data()
        time.sleep(3600)  # 1 jam
