# emotion_detection.py
"""
Minimal Watson Emotion Detection caller (v1) for Task 2.
Returns raw response text from the Skills Network Watson Emotion API.
"""

from typing import Any
import json
import requests
from typing import Dict, Optional

URL = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

def _empty_result() -> Dict[str, Optional[float]]:
    """Standard empty result for invalid/blank text."""
    return {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }

def emotion_detector(text_to_analyze: str) -> Dict[str, Optional[float]]:
    payload = {"raw_document": {"text": text_to_analyze}}
    resp = requests.post(URL, headers=HEADERS, json=payload, timeout=30)

    # Blank input per project spec → return None values
    if resp.status_code == 400:
        return _empty_result()

    resp.raise_for_status()
    data = resp.json()

    try:
        emotions = data["emotionPredictions"][0]["emotion"]
        anger = float(emotions.get("anger", 0.0))
        disgust = float(emotions.get("disgust", 0.0))
        fear = float(emotions.get("fear", 0.0))
        joy = float(emotions.get("joy", 0.0))
        sadness = float(emotions.get("sadness", 0.0))
        scores = {
            "anger": anger,
            "disgust": disgust,
            "fear": fear,
            "joy": joy,
            "sadness": sadness,
        }
        dominant = max(scores, key=scores.get)
        return {**scores, "dominant_emotion": dominant}
    except Exception:
        return _empty_result()