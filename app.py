
#from waitress import serve
from PIL import Image
from flask import Flask, render_template, request, Response
import json
import service.detect_image as DetectImage
app = Flask(__name__)

@app.route("/")
def root():
    return render_template('index.html')

@app.route("/detect-license-plate", methods =["GET"])
def page_detect_license_plate():
    return render_template('detect_license_plate.html')

def root():
    return render_template('index.html')


@app.route("/detect", methods=["POST"])
def detect():
    buf = request.files["image_file"]
    type = request.form.get("type_detect")
    boxes = DetectImage.detect_objects_on_image(Image.open(buf.stream),int(type))
    return Response(
      json.dumps(boxes),
      mimetype='application/json'
    )

@app.route("/detect-license-plate", methods=["POST"])
def detect_license_plate():
    buf = request.files["image_file"]
    boxes = DetectImage.handle_detect_license_plate(Image.open(buf.stream))
    return Response(
      json.dumps(boxes),
      mimetype='application/json'
    )

#serve(app, host='0.0.0.0', port=8080)
