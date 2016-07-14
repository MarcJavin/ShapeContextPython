
import glob
import os
import pickle
import Shape
from ShapeComparator import ShapeComparator
import numpy as np
import re
import cv2

PATH = "/home/markus/Desktop/ShapeContextPython/"

def train():
    for f in glob.glob(os.path.join("Training_set/", "*")):

        points = pickle.load(open(f,"rb"))
        f = re.sub("Training_set","",f)
        shape = Shape.Shape(f,points)
        shape.compute_histograms()
        shape.serialize("Trained_set/")

        img = np.zeros((ShapeComparator.HEIGHT,ShapeComparator.WIDTH,3), np.uint8)
        shape.print_picture_lines(img,(0,255,0))
        cv2.imwrite(PATH + shape.name+".jpg", img)

def main():
    d1 = Shape.Shape.deserialize("disgust0:0","Trained_set/")
    d2 = Shape.Shape.deserialize("disgust20:0","Trained_set/")
    f = Shape.Shape.deserialize("fear0:0","Trained_set/")

    prefix = "/home/markus/Desktop/ShapeContextPython/"

    comp = ShapeComparator()
    dd = comp.compare(d1,d2)
    img = comp.print_result(prefix)
    cv2.imwrite(prefix+"dd.jpg", img)
    print dd
    df = comp.compare(d1,f)
    img = comp.print_result(prefix)
    cv2.imwrite(prefix+"df.jpg", img)
    print df
    df2 = comp.compare(d2,f)
    img = comp.print_result(prefix)
    cv2.imwrite(prefix+"df2.jpg", img)
    print df2


    return 0


if __name__ == "__main__":
	main()
