# backend/detector.py

from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path
from typing import Literal, Tuple, List, Dict, Optional

from PIL import Image
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification

logger = logging.getLogger(__name__)

MediaType = Literal["audio", "image", "text"]

# Hugging Face model for deepfake image detection
MODEL_NAME = "prithivMLmods/Deep-Fake-Detector-v2-Model"

# Risk band thresholds (same as main.py & bot.py)
RISK_LOW_THRESHOLD = 40.0
RISK_HIGH_THRESHOLD = 75.0


@lru_cache(maxsize=1)
def get_image_model():
    """
    Lazy-load the image model & processor once.
    This avoids reloading them on every request.
    HUGGINGFACE_API_TOKEN is picked from env automatically.
    """
    logger.info("Loading HF image model: %s", MODEL_NAME)
    processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
    model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)
    model.eval()
    return processor, model


def analyze_image(path: str) -> Tuple[float, List[Dict]]:
    """
    Use a real ViT-based deepfake detector to get a risk score (0-100).
    Score ≈ probability that the image is deepfake.

    Returns:
        score (float), highlights (list[dict])
    """
    highlights: List[Dict] = []

    try:
        processor, model = get_image_model()

        img = Image.open(path).convert("RGB")
        inputs = processor(images=img, return_tensors="pt")

        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=-1)[0]

        id2label = model.config.id2label
        deepfake_idx: Optional[int] = None

        for i, label in id2label.items():
            if "deepfake" in label.lower() or "fake" in label.lower():
                deepfake_idx = int(i)
                break

        if deepfake_idx is not None:
            deepfake_prob = float(probs[deepfake_idx])
        else:
            deepfake_prob = float(probs.max())

        score = deepfake_prob * 100.0

        # Simple explainability based on score band
        if score >= RISK_HIGH_THRESHOLD:
            highlights.append(
                {
                    "span": "Model detected strong deepfake artefacts in this image.",
                    "type": "vision_model",
                    "start": 0,
                    "end": 0,
                }
            )
        elif score >= RISK_LOW_THRESHOLD:
            highlights.append(
                {
                    "span": "Model found some inconsistencies in lighting / texture patterns.",
                    "type": "vision_model",
                    "start": 0,
                    "end": 0,
                }
            )

        return score, highlights

    except Exception as e:
        logger.exception("Image analysis failed: %s", e)
        # Fallback: mid risk with a clear explanation
        score = 50.0
        highlights.append(
            {
                "span": "Vision model failed to analyze image (network or model error).",
                "type": "model_error",
                "start": 0,
                "end": 0,
            }
        )
        return score, highlights


def analyze_audio(path: str) -> Tuple[float, List[Dict]]:
    """
    Placeholder audio deepfake detector.
    You can plug in a real HF audio model later.

    Returns:
        score (float), highlights (list[dict])
    """
    score = 65.0
    highlights = [
        {
            "span": "Audio deepfake detection is currently a placeholder model.",
            "type": "audio_stub",
            "start": 0,
            "end": 0,
        }
    ]
    return score, highlights


def analyze_text(text: str) -> Tuple[float, List[Dict]]:
    """
    Simple heuristic text scam detector.
    Looks for KYC / OTP / links / urgency phrases, etc.

    Returns:
        score (float 0–100), highlights (list[dict])
    """
    text_lower = text.lower()
    highlights: List[Dict] = []
    score = 0.0

    def add(span: str, htype: str):
        nonlocal score
        start = text.find(span)
        if start < 0:
            start = 0
        end = start + len(span)
        highlights.append(
            {"span": span, "type": htype, "start": start, "end": end}
        )
        # Each signal bumps score a bit
        score_add_map = {
            "kyc": 10,
            "otp": 20,
            "bank": 10,
            "link": 15,
            "urgency": 15,
            "threat": 20,
            "upi": 10,
            "refund": 10,
        }
        score += score_add_map.get(htype, 5)

    # KYC keywords
    if "kyc" in text_lower:
        add("KYC", "kyc")
    if "video kyc" in text_lower:
        add("video KYC", "kyc")

    # OTP
    if "otp" in text_lower:
        add("OTP", "otp")
    if "one time password" in text_lower:
        add("one time password", "otp")

    # Bank / payment words
    for word in ["net banking", "upi", "imps", "rtgs", "neft", "account freeze", "account block"]:
        if word in text_lower:
            add(word, "bank")

    # Links
    import re

    url_regex = r"https?://\S+"
    for m in re.finditer(url_regex, text):
        add(m.group(0), "link")

    # Urgency / threats
    for phrase in [
        "within 15 minutes",
        "within 30 minutes",
        "immediately",
        "right now",
        "or your account will be blocked",
        "or it will be blocked",
        "to avoid fir",
    ]:
        if phrase in text_lower:
            add(phrase, "urgency")

    # Refund / lottery style
    for word in ["refund", "prize", "lottery", "cashback"]:
        if word in text_lower:
            add(word, "refund")

    # Clamp score to [0, 100]
    score = max(0.0, min(100.0, score))

    return score, highlights


def detect_deepfake(
    media_type: MediaType,
    path: Optional[str] = None,
    text: Optional[str] = None,
) -> Tuple[float, List[Dict]]:
    """
    Unified entry point used by the API.

    For image/audio: pass media_type + path.
    For text: pass media_type="text" + text.
    Returns:
        score, highlights
    """
    if media_type == "image":
        if not path:
            raise ValueError("path is required for image analysis")
        return analyze_image(path)

    elif media_type == "audio":
        if not path:
            raise ValueError("path is required for audio analysis")
        return analyze_audio(path)

    elif media_type == "text":
        if text is None:
            raise ValueError("text is required for text analysis")
        return analyze_text(text)

    else:
        raise ValueError(f"Unsupported media type: {media_type}")
