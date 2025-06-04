from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, JSONResponse
from sheets import fetch_data, get_cached_data
import uvicorn
import threading
import time

app = FastAPI()

# ✅ Didefinisikan paling awal
def auto_refresh():
    while True:
        print("🔁 Auto-refreshing data from Google Sheets...")
        fetch_data()
        time.sleep(3600)

# ✅ Event startup (dipakai saat deploy di Render)
@app.on_event("startup")
def startup_event():
    fetch_data()
    threading.Thread(target=auto_refresh, daemon=True).start()

@app.api_route("/", methods=["GET", "HEAD"])
def index():
    return {"status": "ok", "message": "Espanso API is running."}

@app.get("/trigger/{trigger}", response_class=PlainTextResponse)
def get_trigger(trigger: str):
    data = get_cached_data() or []
    trigger_full = f"#{trigger}".lower()
    for row in data:
        if row.get("TRIGGER", "").lower() == trigger_full:
            return row.get("REPLACE", "")
    return "❌ Trigger tidak ditemukan"

@app.get("/refresh")
def refresh_data():
    fetch_data()
    return {"status": "✅ Refreshed"}

@app.get("/list", response_class=JSONResponse)
def list_triggers():
    data = get_cached_data() or []
    result = [{"TRIGGER": row.get("TRIGGER"), "REPLACE": row.get("REPLACE")} for row in data]
    return {"count": len(result), "TRIGGER": result}

# ✅ Untuk lokal testing
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
