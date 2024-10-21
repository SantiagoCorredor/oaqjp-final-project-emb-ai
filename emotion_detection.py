import requests
import json

def emotion_detection(text_to_analyse):
    # Define the URL for the sentiment analysis API
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = { "raw_document": { "text": text_to_analyse } }
    response = requests.post(url, json=myobj, headers=header)
    # Parse the response from the API
    formatted_response = json.loads(response.text)
    if response.status_code == 200:
        # Extraer las emociones del primer resultado
        emotions = formatted_response['emotionPredictions'][0]['emotion']
        
        # Determinar la emoción dominante
        dominant_emotion = max(emotions, key=emotions.get)
        
        # Construir el diccionario con el formato solicitado
        result = {
            'anger': emotions.get('anger', 0.0),
            'disgust': emotions.get('disgust', 0.0),
            'fear': emotions.get('fear', 0.0),
            'joy': emotions.get('joy', 0.0),
            'sadness': emotions.get('sadness', 0.0),
            'dominant_emotion': dominant_emotion
        }
    else:
        # En caso de error, devolver valores nulos
        result = {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    return result
    