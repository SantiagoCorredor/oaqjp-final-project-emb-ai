"""
This module implements a Flask web application for emotion detection from text.
"""
import logging
from flask import Flask, render_template, request, jsonify

from EmotionDetection.emotion_detection import emotion_detection

app = Flask("Emotion Detector")

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)

@app.route("/emotionDetector")
def emotion_analyzer():
    """
    Analyze the emotions from the provided text.

    Returns:
        A JSON response containing the detected emotions or an error message.
    """
    # Retrieve the text to analyze from the request arguments
    text_to_analyze = request.args.get('textToAnalyze')
    if not text_to_analyze:
        app.logger.error("There is no text to analyze.")
        return jsonify({"error": "Invalid input! Please provide some text."}), 400

    try:
        response = emotion_detection(text_to_analyze)
        app.logger.debug(f"API response: {response}")

        if response.get('status_code') == 400:
            return jsonify({
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }), 400

        # Extract emotion scores
        emotions = {key: response.get(key) for key in ['anger',
                                                        'disgust',
                                                          'fear',
                                                            'joy',
                                                              'sadness']}
        dominant_emotion = response.get('dominant_emotion')

        if dominant_emotion is None:
            app.logger.error("The dominant emotion is None.")
            return jsonify({"error": "Invalid text! Please try again!"}), 400

        # Prepare the response string with emotion scores
        emotions_str = ", ".join([f"{k}: {v:.2f}" for k, v in emotions.items()])
        return (
            f"The detected emotions are: {emotions_str}. "
            f"The dominant emotion is: {dominant_emotion}."
        )

    except Exception as e:
        app.logger.exception(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/")
def render_index_page():
    """
    Render the main application page.

    Returns:
        The rendered HTML for the index page.
    """
    return render_template('index.html')

if __name__ == "__main__":
    # Run the Flask app on localhost
    app.run(host="0.0.0.0", port=5000)
