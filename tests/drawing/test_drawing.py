from sys import path
path.append('../src')
from database import Database
from image import PartImage
import os
import cv2 as cv
from time import sleep

db = Database(os.environ['databaseURL'])

path_images = './drawing/images/B'
part = db.get_part_by_id('1002')

# get all images in the folder
files = os.listdir(path_images)

for file in files:
    if file.endswith('txt'):
        continue

    file = os.path.join(path_images, file)

    triangles_file = file.replace('.png', '.txt')
    triangles = []
    with open(triangles_file, 'r') as f:
        for line in f:
            line = line.strip('\n')
            line = line.split(',')
            x = int(line[0])
            y = int(line[1])
            triangles.append((x, y))

    # load file into cv2 image
    image = cv.imread(file)
    image = PartImage(image, triangles, part, True)
    image.draw_quadrants()
    image.show()
    image.evaluate_holes()
    sleep(2)
    image.close()
