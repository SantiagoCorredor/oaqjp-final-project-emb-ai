from flask import Flask, render_template, request, jsonify
from EmotionDetection.emotion_detection import emotion_detection
import logging

app = Flask("Emotion Detector")

logging.basicConfig(level=logging.DEBUG)

@app.route("/emotionDetector")
def emotion_analyzer():
    text_to_analyze = request.args.get('textToAnalyze')
    if not text_to_analyze:
        app.logger.error("No se proporcionó texto para analizar.")
        return "Invalid input! Please provide some text.", 400

    try:
        response = emotion_detection(text_to_analyze)
        app.logger.debug(f"Respuesta de la API: {response}")
        if response.get('status_code') == 400:
            return jsonify({
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }), 400
        emotions = {key: response.get(key) for key in ['anger', 'disgust', 'fear', 'joy', 'sadness']}
        dominant_emotion = response.get('dominant_emotion')
        if dominant_emotion is None:
            app.logger.error("La emoción dominante es None.")
            return "Invalid text! Please try again!", 400
        emotions_str = ", ".join([f"{k}: {v:.2f}" for k, v in emotions.items()])
        return (
            f"The detected emotions are: {emotions_str}. "
            f"The dominant emotion is: {dominant_emotion}."
        )

    except Exception as e:
        app.logger.exception(f"Ocurrió un error: {str(e)}")
        return f"An error occurred: {str(e)}", 500

@app.route("/")
def render_index_page():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
