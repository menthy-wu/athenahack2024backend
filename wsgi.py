import os

from flask import Flask, request, jsonify
from drawsy import drawsy
from gesture import gesture
from call import call
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/drawsy", methods=["POST"])
async def drawsyapi():
    image = request.json
    result = await drawsy(image['image'])
    return result

@app.route("/gesture", methods=["POST"])
async def gestureapi():
    image = request.json
    result = await gesture(image['image'])
    return result

@app.route("/call", methods=["POST"])
async def callapi():
    data = request.form
    result = await call(data['audio'],data['contacts'] )
    return result

@app.route("/", methods=["GET"])
async def hello():
    print("hello")
    return jsonify(hello="world")


if __name__ == "__main__":
    app.run( debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))