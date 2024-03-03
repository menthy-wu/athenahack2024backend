import os

from flask import Flask, request

from drawsy import drawsy

app = Flask(__name__)

@app.route("/drawsy", methods=["POST"])
async def drawsyapi():
    image = request.form
    result = await drawsy(image['image'])
    return result

app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))