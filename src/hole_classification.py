import cv2
import numpy as np
from keras.models import load_model

# Load the model
model = load_model('../models/keras_model.h5')
labels = open('../models/labels.txt', 'r').readlines()


def predict_hole_type(hole_image: cv2.Mat):
    image = cv2.resize(hole_image, (224, 224), interpolation=cv2.INTER_AREA)
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    image = (image / 127.5) - 1

    probabilities = model.predict(image, verbose=0)[0]

    probabilities = sorted(
        zip(labels, probabilities),
        key=lambda x: x[1],
        reverse=True
    )

    label = probabilities[0][0].split(' ')[1].strip('\n')
    prob = probabilities[0][1]

    if prob < 0.6:
        label = 'background'

    return label
