from flask import Flask, render_template, request, jsonify
from EmotionDetection.emotion_detection import emotion_detection
import logging

app = Flask("Emotion Detector")

# Configuración del logger para depuración
logging.basicConfig(level=logging.DEBUG)

@app.route("/emotionDetector")
def emotion_analyzer():
    # Recuperar el texto desde los argumentos de la solicitud
    text_to_analyze = request.args.get('textToAnalyze')

    # Verificar si el texto proporcionado es válido
    if not text_to_analyze:
        app.logger.error("No se proporcionó texto para analizar.")
        return "Invalid input! Please provide some text.", 400

    try:
        # Llamar a la función emotion_detection y loggear la respuesta
        response = emotion_detection(text_to_analyze)
        app.logger.debug(f"Respuesta de la API: {response}")

        # Verificar si la respuesta contiene 'emotionPredictions'
        predictions = response.get('emotionPredictions')
        if not predictions or not isinstance(predictions, list):
            app.logger.error("La respuesta no contiene 'emotionPredictions'.")
            return "Error: No emotions found in the response.", 500

        # Extraer emociones y emoción dominante
        emotions = predictions[0].get('emotion', {})
        if not emotions:
            app.logger.error("No se encontraron emociones en la respuesta.")
            return "Error: No emotions found in the response.", 500

        dominant_emotion = max(emotions, key=emotions.get)

        # Formatear la respuesta
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
