from flask import Flask, render_template, request, jsonify
from EmotionDetection.emotion_detection import emotion_detection
import logging

app = Flask("Emotion Detector")

# Configurar el logger para depuración
logging.basicConfig(level=logging.DEBUG)

@app.route("/emotionDetector")
def emotion_analyzer():
    text_to_analyze = request.args.get('textToAnalyze')

    # Verificar si se proporciona texto
    if not text_to_analyze:
        app.logger.error("No se proporcionó texto para analizar.")
        return "Invalid input! Please provide some text.", 400

    try:
        # Llamar a la función emotion_detection y registrar la respuesta
        response = emotion_detection(text_to_analyze)
        app.logger.debug(f"Respuesta de la API: {response}")

        # Extraer emociones y la emoción dominante de la respuesta
        emotions = {key: response[key] for key in ['anger', 'disgust', 'fear', 'joy', 'sadness']}
        dominant_emotion = response.get('dominant_emotion')

        # Verificar que haya emociones y una emoción dominante válida
        if not emotions or not dominant_emotion:
            app.logger.error("No se encontraron emociones o emoción dominante.")
            return "Error: Invalid response from the API.", 500

        # Formatear las emociones para mostrarlas
        emotions_str = ", ".join([f"{k}: {v:.2f}" for k, v in emotions.items()])

        # Devolver la respuesta final
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
