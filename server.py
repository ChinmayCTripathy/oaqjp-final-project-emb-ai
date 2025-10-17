# server.py
"""
Flask web server for the Emotion Detection web app.
"""

from typing import Dict, Optional
from flask import Flask, request, render_template
from EmotionDetection import emotion_detector

app = Flask(__name__)

def format_response(scores: Dict[str, float], dominant: Optional[str]) -> str:
    """Return a formatted string with emotion scores and the dominant emotion."""

    return (
        f"For the given statement, the system response is "
        f"'anger': {scores['anger']}, "
        f"'disgust': {scores['disgust']}, "
        f"'fear': {scores['fear']}, "
        f"'joy': {scores['joy']} and "
        f"'sadness': {scores['sadness']}. "
        f"The dominant emotion is {dominant}."
    )

@app.route("/", methods=["GET"])
def index():
    """Serve the main HTML page."""
    return render_template("index.html")

@app.route("/emotionDetector", methods=["GET", "POST"])
def detect_emotion():
    """
    Handle input text, call emotion_detector, and return formatted response.
    """
    text = request.args.get("textToAnalyze") or request.form.get("textToAnalyze") or ""
    result = emotion_detector(text)

    # Blank-input handling (dominant_emotion == None)
    if result.get("dominant_emotion") is None:
        return "Invalid text! Please try again!", 200

    scores = {
        "anger": result["anger"],
        "disgust": result["disgust"],
        "fear": result["fear"],
        "joy": result["joy"],
        "sadness": result["sadness"],
    }
    return format_response(scores, result["dominant_emotion"]), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
