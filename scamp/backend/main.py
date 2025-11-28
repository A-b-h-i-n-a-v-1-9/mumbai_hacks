import os
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse

from .db import init_db, save_event
from .detector import detect_deepfake

# Threshold you decided
THRESHOLD = 80.0

# Resolve project root (one level above backend/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
UPLOAD_DIR = PROJECT_ROOT / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Scamp Backend", version="0.1.0")


@app.on_event("startup")
def on_startup():
    """
    Called when the server starts.
    Ensures database is ready.
    """
    init_db()


@app.get("/ping")
async def ping():
    """
    Simple health check.
    """
    return {"status": "Scamp API online"}


@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    media_type: str = Form(...),      # "audio" or "image"
    user_id: str = Form(...),
    platform: str = Form("telegram")  # default platform
):
    """
    Analyze uploaded media and return scam risk score.
    Currently uses dummy detector; later we plug in real models.
    """
    media_type = media_type.lower()
    if media_type not in {"audio", "image"}:
        return JSONResponse(
            status_code=400,
            content={"error": "media_type must be 'audio' or 'image'"}
        )

    # Save file to uploads directory
    # e.g. uploads/telegram_<user>_<original_name>
    safe_name = file.filename.replace(" ", "_")
    save_path = UPLOAD_DIR / f"{platform}_{user_id}_{safe_name}"

    with open(save_path, "wb") as f:
        f.write(await file.read())

    # Run detection (currently dummy logic)
    score = detect_deepfake(media_type=media_type, path=str(save_path))

    label = "high_risk" if score >= THRESHOLD else "low_risk"

    # Save to DB
    event_id = save_event(
        user_id=user_id,
        platform=platform,
        media_type=media_type,
        score=score,
        label=label,
        file_path=str(save_path),
    )

    return {
        "event_id": event_id,
        "score": score,
        "label": label,
        "threshold": THRESHOLD,
    }
