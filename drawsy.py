import os
import tensorflow as tf
from dotenv import load_dotenv
from hume import HumeStreamClient
from hume.models.config import FaceConfig
from flask import jsonify 

load_dotenv()
HUME_API_KEY = GCP_PROJECT_ID = os.getenv('HUME_API_KEY')

def process_emotion(image):
    frames = (image['face']['predictions'][0]['emotions'])
    return tf.convert_to_tensor([emotion['score'] for emotion in frames] ) 


async def drawsy(base64image):
    base64image = base64image.encode('utf-8')
    drawsy_model = tf.keras.models.load_model('drawsy.keras')
    client = HumeStreamClient(HUME_API_KEY)
    config = FaceConfig()
    async with client.connect([config]) as socket:
        emotions = await socket.send_bytes(base64image)
        result =  drawsy_model.predict(tf.convert_to_tensor([process_emotion(emotions)]))
        print(type(result[0][0]))
        return jsonify(drawsiness=float(result[0][0]))

