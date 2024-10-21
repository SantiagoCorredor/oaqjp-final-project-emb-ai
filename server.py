from flask import Flask, render_template, request, jsonify
from EmotionDetection.emotion_detection import emotion_detection

app = Flask("Emotion Detector")

@app.route("/emotionDetection")
def emotion_analyzer():
    text_to_analyze = request.args.get('textToAnalyze')

    if not text_to_analyze:
        return "Invalid input! Please provide some text.", 400


    try:
        response = emotion_detection(text_to_analyze)
        predictions = response.get('emotionPredictions')

        if not predictions:
            return "Error: No emotions found in the response.", 500

        emotions = predictions[0].get('emotion', {})
        dominant_emotion = max(emotions, key=emotions.get)

        emotions_str = ", ".join([f"{k}: {v:.2f}" for k, v in emotions.items()])

        return (
            f"The detected emotions are: {emotions_str}. "
            f"The dominant emotion is: {dominant_emotion}."
        )
    
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@app.route("/")
def render_index_page():
    '''Renderiza la página principal de la aplicación'''
    return render_template('index.html')

if __name__ == "__main__":
    '''Ejecuta la aplicación Flask en localhost:5000'''
    app.run(host="0.0.0.0", port=5000)
