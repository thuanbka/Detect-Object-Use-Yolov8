from ultralytics import YOLO

class DetectImage:

    @staticmethod
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

    @staticmethod
    def handle_detect_license_plate(buf):
        model = YOLO("best_license_plate.pt")
        results = model.predict(buf)
        result = results[0]
        output = []
        for box in result.boxes:
            x1, y1, x2, y2 = [
                round(x) for x in box.xyxy[0].tolist()
            ]
            prob = round(box.conf[0].item(), 2)
            output.append([
                x1, y1, x2, y2, result.names[0], prob
            ])
        return output