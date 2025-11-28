from typing import Literal
import random

MediaType = Literal["audio", "image"]


def analyze_image(path: str) -> float:
    """
    TEMP IMPLEMENTATION.
    Return a fake risk score between 0 and 100 for the image.
    Replace later with a real deepfake detection model.
    """
    # For now: deterministic-ish fake score using file name length
    base = len(path) % 40 + 50  # between 50 and 90
    jitter = random.uniform(-5, 5)
    return max(0.0, min(100.0, base + jitter))


def analyze_audio(path: str) -> float:
    """
    TEMP IMPLEMENTATION.
    Return a fake risk score between 0 and 100 for the audio.
    Replace later with a real deepfake/voice model.
    """
    base = (len(path) * 1.3) % 40 + 50
    jitter = random.uniform(-5, 5)
    return max(0.0, min(100.0, base + jitter))


def detect_deepfake(media_type: MediaType, path: str) -> float:
    """
    Unified entry point used by the API.
    """
    if media_type == "image":
        return analyze_image(path)
    elif media_type == "audio":
        return analyze_audio(path)
    else:
        raise ValueError(f"Unsupported media type: {media_type}")
