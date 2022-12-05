from object_detection import ObjectDetection
import cv2 as cv
import os
import time

from database import Database
from image import PartImage

db = Database(os.environ['databaseURL'])
part = db.get_part_by_id('1001')

cap = cv.VideoCapture(1)
prob_threshold = 0.2
nms_threshold = 0.45
model = ObjectDetection('../models', ['Triangles'], prob_threshold)

start_time = 1

while True:
    # get fps
    fps = 1 / (time.time() - start_time)
    start_time = time.time()
    ret, frame = cap.read()
    drawer = frame.copy()

    prediction = model.predict_image(frame)
    triangles = []
    boxes = []
    scores = []

    height, width, _ = frame.shape

    for i in range(len(prediction)):
        box = prediction[i]['boundingBox']
        confidence = prediction[i]['probability']
        x1 = int(box['left'] * width)
        x2 = x1 + int(box['width'] * width)
        y1 = int(box['top'] * height)
        y2 = y1 + int(box['height'] * height)

        box = [x1, y1, x2, y2]

        boxes.append(box)
        scores.append(float(confidence))

    indices = cv.dnn.NMSBoxes(boxes, scores, prob_threshold, nms_threshold)

    selected_boxes = [boxes[i] for i in indices]
    selected_scores = [scores[i] for i in indices]

    for i in range(len(selected_boxes)):
        box = selected_boxes[i]
        score = selected_scores[i]
        x1, y1, x2, y2 = box
        center = ((x1 + x2) // 2, (y1 + y2) // 2)
        triangles.append(center)
        cv.rectangle(drawer, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv.putText(
            drawer,
            f'{score:.2f}',
            (x1, y1),
            cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
            2
        )

    cv.putText(
        drawer,
        f'FPS: {fps:.2f}',
        (10, 30),
        cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
        2
    )

    cv.imshow('frame', drawer)
    key = cv.waitKey(1)
    if key == ord('q'):
        exit()

    if len(triangles) < 4:
        continue

    try:
        right = False
        counter = 0
        image = PartImage(frame, triangles, part, True)
        while not right:
            image.draw_quadrants()
            image.show()
            right = image.evaluate_holes()

            if right:
                print('Yeeea! Right!')
                break

            if counter == 3:
                print('Too many tries, wrong part!!')
                break

            print('oops, lets try again')
            image.rotate_part()
            counter += 1

    except Exception as e:
        print(e)
        continue
