import unittest
from EmotionDetection.emotion_detection import emotion_detection 
class TestEmotionDetection(unittest.TestCase):
    def test_joy(self):
        """Test for the joy emotion."""
        result = emotion_detection("I am glad this happened")
        self.assertEqual(
            result['dominant_emotion'], 
            'joy', 
            f"Fail at 'I am glad this happened': expected 'joy' but instead get '{result['dominant_emotion']}'."
        )
    def test_anger(self):
        """Test for the anger emotion."""
        result = emotion_detection("I am really mad about this")
        self.assertEqual(
            result['dominant_emotion'], 
            'anger', 
            f"Fail at 'I am really mad about this': expected 'anger' but instead get '{result['dominant_emotion']}'."
        )
    def test_disgust(self):
        """Test for the disgust emotion."""
        result = emotion_detection("I feel disgusted just hearing about this")
        self.assertEqual(
            result['dominant_emotion'], 
            'disgust', 
            f"Fail at 'I feel disgusted just hearing about this': expected 'disgust' but instead get '{result['dominant_emotion']}'."
        )
    def test_sadness(self):
        """Test for the sadness emotion."""
        result = emotion_detection("I am so sad about this")
        self.assertEqual(
            result['dominant_emotion'], 
            'sadness', 
            f"Fail at 'I am so sad about this': expected 'sadness' but instead get '{result['dominant_emotion']}'."
        )
    def test_fear(self):
        """Test for the fear emotion."""
        result = emotion_detection("I am really afraid that this will happen")
        self.assertEqual(
            result['dominant_emotion'], 
            'fear', 
            f"Fail at 'I am really afraid that this will happen': expected 'fear' but instead get '{result['dominant_emotion']}'."
        )
if __name__ == '__main__':
    unittest.main()
