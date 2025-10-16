# emotion_detection.py
"""
Minimal Watson Emotion Detection caller (v1) for Task 2.
Returns raw response text from the Skills Network Watson Emotion API.
"""

from typing import Any
import json
import requests

URL = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

def emotion_detector(text_to_analyze: str) -> Any:
    """
    Call the Watson NLP EmotionPredict endpoint and return raw response text.
    """
    payload = {"raw_document": {"text": text_to_analyze}}
    resp = requests.post(URL, headers=HEADERS, json=payload, timeout=30)
    # For Task 2, return the raw text (as required).
    return resp.text
