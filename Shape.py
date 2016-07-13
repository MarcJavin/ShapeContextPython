
import numpy as np
import cv2
import math
import pickle

class Shape :

    PATH = "/home/markus/Desktop/ShapeContextPython/"
    WIDTH = 1000
    HEIGHT = 1000
    FACTOR = 10

    def __init__(self, name, points, nb_theta=12, thresholds_r=[0.125,0.25,0.5,1,2]):
        self.name = name
        self.points = np.array(np.int32(points))
        self.nb_theta = nb_theta
        self.thresholds_r = thresholds_r
        self.histograms = np.zeros((len(points),len(thresholds_r),nb_theta))


    def compute_histograms(self):
        nb_points = len(self.points)
        distances = np.zeros((nb_points,nb_points))
        angles = np.zeros((nb_points,nb_points))
        mean_distance = 0

        for n1 in xrange(nb_points) :
            for n2 in xrange(n1+1,nb_points) :

                # compute distance

                dx = self.points[n2][0]-self.points[n1][0]
                dy = self.points[n2][1]-self.points[n1][1]
                distances[n1,n2] = math.sqrt(dx*dx + dy*dy)

                #compute angle
                if(dx == 0):
                    if(dy == 0):
                        angles[n1,n2]=0
                    elif(dy < 0):
                        angles[n1,n2]=3*math.pi/2
                    elif(dy > 0):
                        angles[n1,n2]=math.pi/2
                else:
                    angles[n1,n2] = np.arctan(dy/dx)
                    if(dx<0):
                        angles[n1,n2] += math.pi/2
                    elif(dy<0):
                        angles[n1,n2] += math.pi

                mean_distance += 2 * distances[n1,n2]

        #normalize distance

        mean_distance /= (nb_points*nb_points)
        distances /= mean_distance

        #discretize distance and angle

        for n1 in xrange(nb_points) :
            for n2 in xrange(n1,nb_points) :
                if(distances[n1,n2]>self.thresholds_r[-1]):
                    distances[n1,n2]=-1
                    distances[n2,n1]=-1
                else:
                    for t in xrange(len(self.thresholds_r)) :
                        if(distances[n1,n2]<=self.thresholds_r[t]):
                            distances[n1,n2]=t
                            distances[n2,n1]=t
                            break


                angles[n1,n2] = (math.floor)(angles[n1,n2]/(2*math.pi/self.nb_theta))
                if(angles[n1,n2]>5):
                    angles[n2,n1] = angles[n1,n2]-6
                else:
                    angles[n2,n1] = angles[n1,n2]+6

        for n1 in xrange(nb_points):
            for n2 in xrange(nb_points):
                if(n1!=n2):
                    bin_r = distances[n1,n2]
                    if(bin_r!=-1):
                        bin_theta = angles[n1,n2]
                        self.histograms[n1,bin_r,bin_theta]+=1


    def serialize(self, prefix=""):
        pickle.dump(self, open( prefix+self.name, "wb" ))

    @staticmethod
    def deserialize(fic_name):
        return pickle.load( open( fic_name,"rb" ) )


    def print_picture(self):
        img = np.zeros((Shape.HEIGHT,Shape.WIDTH,3), np.uint8)
        points = Shape.FACTOR*self.points
        cv2.fillPoly(img, np.int32([points]), (0,255,255))
        cv2.imwrite(Shape.PATH+self.name+".jpg", img)

    def print_picture_lines(self,img,color):
        points = Shape.FACTOR*self.points
        for n in xrange(len(points)):
            cv2.line(img,(points[n-1][0],points[n-1][1]),(points[n][0],points[n][1]),color,3)


def main():
    k = Shape("yvonne",[(1,1),(2,2),(1,3),(4,1)])
    k.compute_histograms()
    k.serialize()

    k.print_picture()

    j = pickle.load( open( "yvonne", "rb" ) )
    print j.histograms
    return 0


if __name__ == "__main__":
	main()
