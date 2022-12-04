import tensorflow as tf
import numpy as np
import cv2 as cv


def crop_center(img, cropx, cropy):
    h, w = img.shape[:2]
    startx = w//2-(cropx//2)
    starty = h//2-(cropy//2)
    return img[starty:starty+cropy, startx:startx+cropx]


model_path = 'litelite.tflite'
labels_path = 'labels.txt'

interpreter = tf.lite.Interpreter(model_path=model_path)

cap = cv.VideoCapture(1)

while True:
    ret, frame = cap.read()

    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    frame = crop_center(frame, 720, 720)
    frame = cv.resize(frame, (416, 416))
    input_data = np.expand_dims(frame, axis=0)
    input_data = (np.float32(input_data) - 127.5) / 127.5

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    print(len(output_details))
    output_data = interpreter.get_tensor(output_details[0]['index'])[0]
    # print(output_data)

    cv.imshow('frame', frame)
    key = cv.waitKey(1)
    if key == ord('q'):
        exit()
