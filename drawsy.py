import os
import tensorflow as tf
from dotenv import load_dotenv
from hume import HumeStreamClient
from hume.models.config import FaceConfig
from flask import jsonify 
import base64
import numpy as np
import cv2

load_dotenv()
HUME_API_KEY = GCP_PROJECT_ID = os.getenv('HUME_API_KEY')
drawsy_model = tf.keras.models.load_model('drawsy.keras')

# def process_emotion(image):
#     frames = (image['face']['predictions'][0]['emotions'])
#     return tf.convert_to_tensor([emotion['score'] for emotion in frames] ) 

file = open("image.jpg", "wb")
async def drawsy(base64image):
    # print(base64image)
    client = HumeStreamClient(HUME_API_KEY)
    config = FaceConfig()
    async with client.connect([config]) as socket:
        image = base64.b64decode(base64image)
        nparr = np.frombuffer(image, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        jpg_as_text = base64.b64encode(cv2.imencode('.jpg', img)[1].tostring())
        emotions = await socket.send_bytes(jpg_as_text)
        try:
            frames = (emotions['face']['predictions'][0]['emotions'])
            arr = tf.convert_to_tensor([emotion['score'] for emotion in frames] ) 
            result =  drawsy_model.predict(tf.convert_to_tensor([arr]))
            print(float(result[0][0]))
            return jsonify(drawsiness=float(result[0][0]))
        except:
            return jsonify(drawsiness=0)
        
        

