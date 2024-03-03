import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import base64
from flask import jsonify 

base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)



async def gesture(base64Image):
    binary = base64.b64decode(base64Image)
    image = np.asanyarray(bytearray(binary), dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = mp.Image( image_format=mp.ImageFormat.SRGB, data=np.asarray(image))

    recognition_result = recognizer.recognize(image)
    gesture = ""
    score = 0
    try:
        gesture = (recognition_result.gestures[0][0].category_name)
        score = (recognition_result.gestures[0][0].score)
    except:
        gesture = ""
        score = 0
    print(gesture)
    return  jsonify(gesture=gesture,score=score)