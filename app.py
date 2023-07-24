from ultralytics import YOLO
from waitress import serve
from PIL import Image
from flask import Flask, render_template, request, Response
import json

#import logging

#model = YOLO("yolov8m.pt")
app = Flask(__name__)


@app.route("/")
def root():
  #print(model)
  return render_template('index.html')


@app.route("/detect", methods=["POST"])
def detect():
  buf = request.files["image_file"]
  type_image = request.form.get("type_detect")
  boxes = detect_objects_on_image(Image.open(buf.stream),int(type_image))
  return Response(
    json.dumps(boxes),
    mimetype='application/json'
  )


def detect_objects_on_image(buf, type_image):
  model = YOLO("yolov8m.pt")
  print("Type:")
  print(type_image)
  result = None
  try:
    print("Run with CPU.")
    #logging.info('Run with CPU.')
    results = model.predict(source = buf, device='cpu',imgsz=320)
    result = results[0]
  except Exception as ex:
    print(ex)
  print("Predict done!!!")
  output = []
  if result != None:
    for box in result.boxes:
        x1, y1, x2, y2 = [
          round(x) for x in box.xyxy[0].tolist()
        ]
        class_id = box.cls[0].item()
        print(class_id)
        if class_id == type_image:
            prob = round(box.conf[0].item(), 2)
            output.append([
              x1, y1, x2, y2, result.names[class_id], prob
            ])
  return output

# import resource 
 
# def limit_memory(maxsize): 
#     soft, hard = resource.getrlimit(resource.RLIMIT_AS) 
#     resource.setrlimit(resource.RLIMIT_AS, (maxsize, hard)) 
# limit_memory(512)
serve(app, host='0.0.0.0', port=8080)
#gunicorn app:app  --workers 5 --timeout 100
#https://stackoverflow.com/questions/67637004/gunicorn-worker-terminated-with-signal-9
