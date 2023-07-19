from ultralytics import YOLO
#from waitress import serve
from PIL import Image
from flask import Flask, render_template, request, Response
import json
app = Flask(__name__)


app = Flask(__name__)

@app.route("/")
def root():
    return render_template('index.html')


@app.route("/detect", methods=["POST"])
def detect():
    buf = request.files["image_file"]
    type = request.form.get("type_detect")
    boxes = detect_objects_on_image(Image.open(buf.stream),int(type))
    return Response(
      json.dumps(boxes),
      mimetype='application/json'
    )


def detect_objects_on_image(buf, type):
    model = YOLO("yolov8m.pt")
    results = model.predict(buf)
    result = results[0]
    output = []
    for box in result.boxes:
        x1, y1, x2, y2 = [
          round(x) for x in box.xyxy[0].tolist()
        ]
        class_id = box.cls[0].item()
        if class_id == type:
            prob = round(box.conf[0].item(), 2)
            output.append([
              x1, y1, x2, y2, result.names[class_id], prob
            ])
    return output

#serve(app, host='0.0.0.0', port=8080)
