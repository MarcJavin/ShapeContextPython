
import glob
import os
import pickle
import Shape
from ShapeComparator import ShapeComparator
import numpy as np
import re
import cv2

PATH = "/home/markus/Desktop/ShapeContextPython/"

def main():
    for f in glob.glob(os.path.join("Training_set/", "*")):

        points = pickle.load(open(f,"rb"))
        f = re.sub("Training_set","",f)
        shape = Shape.Shape(f,points)
        shape.compute_histograms()
        shape.serialize("Trained_set/")

        img = np.zeros((ShapeComparator.HEIGHT,ShapeComparator.WIDTH,3), np.uint8)
        shape.print_picture_lines(img,(0,255,0))
        cv2.imwrite(PATH + shape.name+".jpg", img)





    return 0


if __name__ == "__main__":
	main()
