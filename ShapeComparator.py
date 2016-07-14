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

        cost_matrix = basic_cost_matrix.copy()

        associations = self.hungarian_algorithm(cost_matrix, l1, l2)

        self.associations = associations
        final_cost = 0
        for a in associations:
            final_cost+=basic_cost_matrix[a[0],a[1]]

        return final_cost


    def hungarian_algorithm(self, cost_matrix, l1, l2):

        #Step 0 : create zeros

        nb_connections = min(l1,l2)

        for n1 in xrange(l1):
            cost_matrix[n1,:]-=np.amin(cost_matrix[n1,:])
        for n2 in xrange(l2):
            cost_matrix[:,n2]-=np.amin(cost_matrix[:,n2])

        #Step 1

        nb_zero_lines = np.zeros((l1))
        zero_lines = np.zeros((l1))
        zero_columns = np.zeros((l2))
        selected_zeros = np.zeros((l1,l2))
        associations = []
        nb_zeros = 0

        #count zeros

        for n1 in xrange(l1):
            for n2 in xrange(l2):
                if(cost_matrix[n1,n2]==0):
                    nb_zero_lines[n1]+=1

        #Step 2
        #select zeros

        for k in xrange(l1):
            n1 = np.argmin(nb_zero_lines)
            nb_zero_lines[n1]=l2
            for n2 in xrange(l2):
                if(cost_matrix[n1,n2]==0):
                    if(zero_lines[n1]==0 and zero_columns[n2]==0):
                        associations.append([n1,n2])
                        selected_zeros[n1,n2]=1
                        zero_lines[n1]=1
                        zero_columns[n2]=1
                        nb_zeros += 1
                        break


        #Step 3

        if(nb_zeros != nb_connections):
            marked_lines = np.zeros((l1))
            marked_columns = np.zeros((l2))

            #all lines having no selected zero
            for n1 in xrange(l1):
                if(zero_lines[n1]==0):
                    marked_lines[n1] = 1

            non_covered_zero = True
            while(non_covered_zero):
                non_covered_zero = False

                #all columns having a no selected zero on a marked line
                for n1 in xrange(l1):
                    if(marked_lines[n1] == 1):
                        for n2 in xrange(l2):
                            if(marked_columns[n2]==0 and cost_matrix[n1,n2]==0 and
                            selected_zeros[n1,n2]==0):
                                marked_columns[n2]=1
                                non_covered_zero = True

                #all lines having a selected zero on a marked column
                for n2 in xrange(l2):
                    if(marked_columns[n2] == 1):
                        for n1 in xrange(l1):
                            if(marked_lines[n1]==0 and cost_matrix[n1,n2]==0 and
                            selected_zeros[n1,n2]==1):
                                marked_lines[n1]=1
                                non_covered_zero = True

            #minimum of the non marked elements
            mini = 1000
            for n1 in xrange(l1):
                for n2 in xrange(l2):
                    if(marked_lines[n1]==1 and marked_columns[n2]==0 and cost_matrix[n1,n2]<mini):
                        mini = cost_matrix[n1,n2]

            ##add mini to the non marked elements, substract if from the double marked ones
            for n1 in xrange(l1):
                for n2 in xrange(l2):
                    if(marked_lines[n1]==1 and marked_columns[n2]==0):
                        cost_matrix[n1,n2]-=mini
                    elif(marked_lines[n1]==0 and marked_columns[n2]==1):
                        cost_matrix[n1,n2]+=mini

            return self.hungarian_algorithm(cost_matrix, l1, l2)

        return associations


    def print_result(self, prefix=""):
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
        cv2.imwrite(prefix+self.shape1.name+"-"+self.shape2.name+".jpg", img)
        return img




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


    mat = np.array([[17,15,9,5,12],[16,16,10,5,10],[12,15,14,11,5],[4,8,14,17,13],[13,9,8,12,17]])
    comparator.hungarian_algorithm(mat,5,5)

    mat = np.array([[80,40,50,46],[40,70,20,25],[30,10,20,30],[35,20,25,30]])
    comparator.hungarian_algorithm(mat,4,4)


    return 0


if __name__ == "__main__":
	main()
