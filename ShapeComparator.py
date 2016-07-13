from Shape import Shape
import numpy as np
import cv2

class ShapeComparator :

    WIDTH = 1000
    HEIGHT = 1000
    FACTOR = 100

    def __init__(self):
        self.shape1 = None
        self.shape2 = None
        self.associations = None
        return


    def compare(self,shape1, shape2):

        self.shape1=shape1
        self.shape2=shape2


        if(shape1.thresholds_r!=shape2.thresholds_r or shape1.nb_theta!=shape2.nb_theta):
            print "Error : The shapes have not the same configurations"
            return 1

        l1 = len(shape1.points)
        l2 = len(shape2.points)
        nb_connections = min(l1,l2)
        basic_cost_matrix = np.zeros((l1,l2))

        for n1 in xrange(l1):
            for n2 in xrange(l2):
                for r in xrange(len(shape1.thresholds_r)):
                    for theta in xrange(shape1.nb_theta):
                        value1 = shape1.histograms[n1,r,theta]
                        value2 = shape2.histograms[n2,r,theta]
                        summ = value1+value2
                        if(summ!=0):
                            diff = value1-value2
                            basic_cost_matrix[n1,n2] += 0.5*(diff*diff)/(value1+value2)

        #Hungarian algorithm
        #Step 0

        cost_matrix = basic_cost_matrix

        for n1 in xrange(l1):
            cost_matrix[n1,:]-=np.amin(cost_matrix[n1,:])

        #Step 1

        zero_lines = np.zeros((l1))
        zero_columns = np.zeros((l2))
        associations = []
        nb_zeros = 0

        for n1 in xrange(l1):
            for n2 in xrange(l2):
                if(cost_matrix[n1,n2]==0):
                    if(zero_lines[n1]==0 and zero_columns[n2]==0):
                        zero_lines[n1]=1
                        zero_columns[n2]=1
                        associations.append([n1,n2])
                        nb_zeros += 1

        #Step 2

        if(nb_zeros != nb_connections):
            for n2 in xrange(l2):
                if(zero_columns[n2]==0):
                    cost_matrix[:,n2]-=np.amin(cost_matrix[:,n2])
                    for n1 in xrange(l1):
                        if(cost_matrix[n1,n2]==0):
                            if(zero_lines[n1]==0):
                                zero_lines[n1]=1
                                zero_columns[n2]=1
                                associations.append([n1,n2])
                                nb_zeros += 1

        #Step 3

        if(nb_zeros != nb_connections):
            print "Dur dur dur..."
            zero_lines3 = np.zeros((l1))
            zero_columns3 = zero_columns
            non_covered_zero is True
            while(non_covered_zero):
                non_covered_zero is False
                for n1 in xrange(l1):
                    if(zero_lines[n1]==1):
                        for n2 in xrange(l2):
                            if(zero_columns3[n2]==0):
                                for n22 in xrange(l2):
                                    if(zero_columns[n22]==1):
                                        zero_lines3[n1]=1
                                        zero_columns3[n22]=0
                                        non_covered_zero is True

        self.associations = associations
        final_cost = 0
        for a in associations:
            final_cost+=basic_cost_matrix[a[0],a[1]]

        return final_cost


    def print_result(self):
        img = np.zeros((ShapeComparator.HEIGHT,ShapeComparator.WIDTH,3), np.uint8)
        self.shape1.print_picture_lines(img,(0,255,0))
        self.shape2.print_picture_lines(img,(0,0,255))
        for a in self.associations:
            a0 = Shape.FACTOR*self.shape1.points[a[0]][0]
            a1 = Shape.FACTOR*self.shape1.points[a[0]][1]
            b0 = Shape.FACTOR*self.shape2.points[a[1]][0]
            b1 = Shape.FACTOR*self.shape2.points[a[1]][1]
            cv2.line(img,(a0,a1),(b0,b1),(0,255,255))
            cv2.circle(img,(a0,a1),6,(0,255,255))
            cv2.circle(img,(b0,b1),6,(0,255,255))
        cv2.imwrite(self.shape1.name+"-"+self.shape2.name+".jpg", img)





def main():
    k = Shape("yvonne",[[1,1],[2,2],[1,3],[4,1]])
    k.compute_histograms()
    k.serialize()
    k.print_picture()

    j = Shape.deserialize("yvonne")

    k2 = Shape("jeanguy",[[5,2],[3,3],[4,4],[8,2]])
    k2.compute_histograms()

    k2.print_picture()

    comparator = ShapeComparator()
    answer = comparator.compare(k,k2)
    comparator.print_result()
    print answer

    return 0


if __name__ == "__main__":
	main()
