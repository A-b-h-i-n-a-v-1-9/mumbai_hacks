# scamp/backend/main.py

from pathlib import Path
import logging
from typing import Any, Tuple

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .db import init_db, save_event
from .detector import detect_deepfake

logger = logging.getLogger(__name__)

# ---- Risk thresholds for bucketing ----
RISK_LOW_THRESHOLD = 40.0    # 0–40  => "low"
RISK_HIGH_THRESHOLD = 75.0   # 40–75 => "medium", 75+ => "high"

# Resolve project root (one level above backend/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
UPLOAD_DIR = PROJECT_ROOT / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Scamp Backend", version="0.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # for dev; later you can restrict
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ---------- Helpers ----------

def bucketize_risk(score: float) -> str:
    """
    Map raw score 0–100 into 'low' / 'medium' / 'high'.
    """
    # Make sure score is a float, not a tuple etc.
    try:
        score = float(score)
    except Exception:
        logger.warning("bucketize_risk got non-numeric score=%r; forcing 0.0", score)
        score = 0.0

    if score >= RISK_HIGH_THRESHOLD:
        return "high"
    elif score >= RISK_LOW_THRESHOLD:
        return "medium"
    else:
        return "low"


def normalize_detector_output(detector_result: Any) -> Tuple[float, str, list]:
    """
    Accepts whatever detect_deepfake returns and normalizes it to:
        (score: float, risk: str, highlights: list[dict])
    This is robust to older/newer detector implementations.
    """
    score: float
    highlights: list = []

    # Case 1: detector returns (score, highlights)
    if isinstance(detector_result, tuple) and len(detector_result) >= 1:
        score = float(detector_result[0])
        if len(detector_result) >= 2:
            maybe_h = detector_result[1]
            if isinstance(maybe_h, list):
                highlights = maybe_h
            elif isinstance(maybe_h, dict):
                highlights = [maybe_h]
    # Case 2: detector returns dict
    elif isinstance(detector_result, dict):
        score = float(detector_result.get("score", 0.0))
        maybe_h = detector_result.get("highlights")
        if isinstance(maybe_h, list):
            highlights = maybe_h
        elif isinstance(maybe_h, dict):
            highlights = [maybe_h]
    # Case 3: plain scalar score
    else:
        score = float(detector_result)

    risk = bucketize_risk(score)
    return score, risk, highlights


# ---------- FastAPI lifecycle ----------

@app.on_event("startup")
def on_startup():
    """Called when the server starts. Ensures database is ready."""
    init_db()


@app.get("/ping")
async def ping():
    """Simple health check."""
    return {"status": "Scamp API online"}


# ---------- Media analysis (image/audio) ----------

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    media_type: str = Form(...),      # "audio" or "image"
    user_id: str = Form(...),
    platform: str = Form("telegram"),  # default platform
):
    """
    Analyze uploaded media (image/audio) and return scam/deepfake risk score.

    Response JSON:
    {
        "event_id": int,
        "score": float,
        "risk": "low" | "medium" | "high",
        "thresholds": {"low": 40.0, "high": 75.0},
        "highlights": [ ... ]   # optional, for explainability
    }
    """
    media_type = media_type.lower()
    if media_type not in {"audio", "image"}:
        return JSONResponse(
            status_code=400,
            content={"error": "media_type must be 'audio' or 'image' for /analyze"},
        )

    safe_name = file.filename.replace(" ", "_") if file.filename else "upload.bin"
    save_path = UPLOAD_DIR / f"{platform}_{user_id}_{safe_name}"

    # Save file to disk
    try:
        with open(save_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        logger.exception("Failed to save uploaded file: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": "failed to save uploaded file"},
        )

    # Run detection
    try:
        detector_result = detect_deepfake(media_type=media_type, path=str(save_path))
        score, risk, highlights = normalize_detector_output(detector_result)
        logger.info(
            "[DETECT_MEDIA] user=%s media=%s score=%.2f risk=%s file=%s",
            user_id,
            media_type,
            score,
            risk,
            save_path,
        )
    except Exception as e:
        logger.exception("Detection failed: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": "detection failed"},
        )

    # Label used for DB – keep string-y for now, 3‑way
    label = f"{risk}_risk"  # "low_risk" / "medium_risk" / "high_risk"

    # Save to DB
    try:
        event_id = save_event(
            user_id=user_id,
            platform=platform,
            media_type=media_type,
            score=score,
            label=label,
            file_path=str(save_path),
        )
    except Exception as e:
        logger.exception("Failed to save event to DB: %s", e)
        event_id = -1

    return {
        "event_id": event_id,
        "score": score,
        "risk": risk,
        "thresholds": {
            "low": RISK_LOW_THRESHOLD,
            "high": RISK_HIGH_THRESHOLD,
        },
        "highlights": highlights,
    }


# ---------- Text analysis ----------

@app.post("/analyze_text")
async def analyze_text(
    text: str = Form(...),
    user_id: str = Form(...),
    platform: str = Form("telegram"),
):
    """
    Analyze plain text (e.g., chat message) for scam risk.

    Response JSON mirrors /analyze:
    {
        "event_id": int,
        "score": float,
        "risk": "low" | "medium" | "high",
        "thresholds": {"low": 40.0, "high": 75.0},
        "highlights": [ ... ]   # e.g. suspicious links, OTP mentions, KYC, etc.
    }
    """
    text = (text or "").strip()
    if not text:
        return JSONResponse(
            status_code=400,
            content={"error": "text must not be empty"},
        )

    try:
        detector_result = detect_deepfake(media_type="text", text=text)
        score, risk, highlights = normalize_detector_output(detector_result)
        logger.info(
            "[DETECT_TEXT] user=%s score=%.2f risk=%s len=%d",
            user_id,
            score,
            risk,
            len(text),
        )
    except Exception as e:
        logger.exception("Text detection failed: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": "text detection failed"},
        )

    label = f"{risk}_risk"

    try:
        event_id = save_event(
            user_id=user_id,
            platform=platform,
            media_type="text",
            score=score,
            label=label,
            file_path="",  # no file path for text-only
        )
    except Exception as e:
        logger.exception("Failed to save text event to DB: %s", e)
        event_id = -1

    return {
        "event_id": event_id,
        "score": score,
        "risk": risk,
        "thresholds": {
            "low": RISK_LOW_THRESHOLD,
            "high": RISK_HIGH_THRESHOLD,
        },
        "highlights": highlights,
    }
from fastapi.responses import FileResponse
from .db import init_db, save_event, get_event
from .reporting import build_pdf_report

REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_DIR.mkdir(exist_ok=True)

@app.get("/report/{event_id}")
async def get_report(event_id: int):
    """
    Build + return a PDF report for the given event_id.
    """
    event = get_event(event_id)
    if not event:
        return JSONResponse(
            status_code=404,
            content={"error": f"event {event_id} not found"},
        )

    pdf_path = REPORT_DIR / f"scamp_report_{event_id}.pdf"

    try:
        build_pdf_report(event, pdf_path)
    except Exception as e:
        logger.exception("Failed to build PDF report for event %s: %s", event_id, e)
        return JSONResponse(
            status_code=500,
            content={"error": "report generation failed"},
        )

    return FileResponse(
        path=pdf_path,
        filename=f"scamp_report_{event_id}.pdf",
        media_type="application/pdf",
    )
