'''Executing this function initiates the application of emotion
   detection to be executed over the Flask channel and deployed on
   localhost:5000.
'''
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detection

app = Flask("Emotion Detector")

@app.route("/emotionDetection")
def emotion_analyzer():
    text_to_analyze = request.args.get('textToAnalyze')
    if not text_to_analyze:
        return "Invalid input! Please provide some text."

    response = emotion_detection(text_to_analyze)

    emotions = response.get('emotionPredictions')[0].get('emotion')
    dominant_emotion = max(emotions, key=emotions.get)

    emotions_str = ", ".join([f"{k}: {v:.2f}" for k, v in emotions.items()])

    return (
        f"The detected emotions are: {emotions_str}. "
        f"The dominant emotion is: {dominant_emotion}."
    )

@app.route("/")
def render_index_page():
    ''' This function initiates the rendering of the main application
        page over the Flask channel
    '''
    return render_template('index.html')

if __name__ == "__main__":
    ''' This function executes the Flask app and deploys it on localhost:5000
    '''
    app.run(host="0.0.0.0", port=5000)
