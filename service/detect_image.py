from ultralytics import YOLO
import easyocr
from numpy import asarray
model_yolo = YOLO("yolov8m.pt")
model_license_plate = YOLO("best_license_plate.pt")
reader = easyocr.Reader(['en'], gpu=False)

def detect_objects_on_image(buf, type):
    results = model_yolo.predict(buf)
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

def handle_detect_license_plate(buf):
    results = model_license_plate.predict(buf, conf=0.6)
    result = results[0]
    output = []
    for box in result.boxes:
        x1, y1, x2, y2 = [
            round(x) for x in box.xyxy[0].tolist()
        ]
        license_plate_crop = buf.crop((x1,y1,x2,y2))
        license_plate_crop = asarray(license_plate_crop)
        detections = reader.readtext(license_plate_crop)
        number_license = ""
        if detections:
            for line in detections:
                (coordinates,text,probability) = line
                number_license += (text + " ")
        prob = round(box.conf[0].item(), 2)
        output.append([
            x1, y1, x2, y2, prob, number_license
        ])
    return output


