from typing import Literal
from functools import lru_cache

from PIL import Image
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification

MediaType = Literal["audio", "image"]

# Hugging Face model for deepfake image detection
# This model classifies images as (e.g.) "Realism" vs "Deepfake".
MODEL_NAME = "prithivMLmods/Deep-Fake-Detector-v2-Model"


@lru_cache(maxsize=1)
def get_image_model():
    """
    Lazy-load the image model & processor once.
    This avoids reloading them on every request.
    """
    processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
    model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)
    model.eval()
    return processor, model


def analyze_image(path: str) -> float:
    """
    Use a real ViT-based deepfake detector to get a risk score (0-100).
    Score ≈ probability that the image is deepfake.
    """
    processor, model = get_image_model()

    # Load image
    img = Image.open(path).convert("RGB")

    # Preprocess
    inputs = processor(images=img, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=-1)[0]  # shape: [num_classes]

    # Map model's labels to "deepfake" probability
    id2label = model.config.id2label
    deepfake_idx = None

    for i, label in id2label.items():
        if "deepfake" in label.lower() or "fake" in label.lower():
            deepfake_idx = i
            break

    if deepfake_idx is not None:
        deepfake_prob = float(probs[deepfake_idx])
    else:
        # Fallback: if we don't find a "deepfake" label,
        # just take the highest probability as "risk"
        deepfake_prob = float(probs.max())

    # Convert 0–1 probability to 0–100 risk score
    score = deepfake_prob * 100.0
    return score


# ---------- AUDIO: keep stub for now ----------

def analyze_audio(path: str) -> float:
    """
    TODO: integrate real audio deepfake detector later.

    For now, return a mid–high dummy score so the pipeline
    still works if you ever send audio.
    """
    # You can tune this if you want a different default.
    return 65.0


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
