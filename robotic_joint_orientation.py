import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


class RotMatrix:
    # Used to create initial rotation matrices which are relative to the previous robot frame.
    #
    # objName: string with the name of the object being created. This is used for print statements
    # matrixType: string that defines what type of matrix is being created. Takes lower or uppercase letters
    #             X = X (roll) axis roatation matrix
    #             Y = Y (pitch) axis rotation matrix
    #             Z = Z (yaw) axis rotation matrix
    #             I = identity rotatioin matrix
    # theta: angle (in degrees) being rotated. Do NOT use if matrixType is identity
    def __init__(self, objName, matrixType, theta=None):
        self.objName = objName
        self.matrixType = matrixType.upper()
        if(theta != None):
            self.theta = math.radians(theta)
        else:
            self.theta = None
        
        if(self.matrixType == 'X'):
            self.matrix = [[1,                               0,                               0],
                           [0,  round(math.cos(self.theta), 5), round(-math.sin(self.theta), 5)],
                           [0,  round(math.sin(self.theta), 5),  round(math.cos(self.theta), 5)]]
        elif(self.matrixType == 'Y'):
            self.matrix = [[ round(math.cos(self.theta), 5), 0, round(math.sin(self.theta), 5)],
                           [                              0, 1,                              0],
                           [round(-math.sin(self.theta), 5), 0, round(math.cos(self.theta), 5)]]
        elif(self.matrixType == 'Z'):
            self.matrix = [[round(math.cos(self.theta), 5), round(-math.sin(self.theta), 5), 0],
                           [round(math.sin(self.theta), 5),  round(math.cos(self.theta), 5), 0],
                           [                             0,                               0, 1]]
        elif(self.matrixType == 'I' and self.theta == None):
            self.matrix = [[1, 0, 0],
                           [0, 1, 0],
                           [0, 0, 1]]
        # if the matrixType does not match a pre-defined type
        else:
            print('\nSomething went wrong in the definition of ' + self.objName)

    def print_matrix(self):
        #prints the matrix in handwritten form instead of computer form
        print('Printing: ' + str(self.objName))
        print(*self.matrix, sep="\n") 
        print('\n')
        
        
        
class CalculatedRotMatrix:
    # Used to calculate rotation matrices which are relative to frame 0.
    #
    # objName: string with the name of the object being created. This is used for print statements
    # rm1: relative rotation matrix. R_0x where x is the number of the robot frame which has been calculated up to
    # rm2: the initial rotation matrix which comes sequentially after the R_0x matrix
    def __init__(self, objName, rm1, rm2):
        self.objName = objName
        self.rm1 = rm1
        self.rm2 = rm2
        
        # calclate the resultant relative rotation matrix using dot product
        self.matrix = np.dot(rm1, rm2)

    def print_matrix(self):
        #prints the matrix in handwritten form instead of computer form
        print('Printing: ' + str(self.objName))
        print(self.matrix) 
        print('\n')



def graph_orientation(R):
    # graphs the orientation of the chosen rotation matrix relative to the starting frame R_00
    #
    # the thicker lines are the orientation of R_00
    # the thinner lines are the orientation of R_0x
    #       red line = X axis
    #       blue line = Y axis
    #       green line = Z axis
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    datasets = [{"x":[0,1], "y":[0,0], "z":[0,0], "colour": "red", "lw" : 2},
                {"x":[0,0], "y":[0,1], "z":[0,0], "colour": "blue", "lw" : 2},
                {"x":[0,0], "y":[0,0], "z":[0,1], "colour": "green", "lw" : 2},
                {"x":[0,(R.matrix[0][0])], "y":[0,(R.matrix[1][0])], "z":[0,(R.matrix[2][0])], "colour": "red", "lw" : 1},
                {"x":[0,(R.matrix[0][1])], "y":[0,(R.matrix[1][1])], "z":[0,(R.matrix[2][1])], "colour": "blue", "lw" : 1},
                {"x":[0,(R.matrix[0][2])], "y":[0,(R.matrix[1][2])], "z":[0,(R.matrix[2][2])], "colour": "green", "lw" : 1}]

    for dataset in datasets:
        ax.plot(dataset["x"], dataset["y"], dataset["z"], color=dataset["colour"], linewidth=dataset["lw"])

    fig.suptitle('Robotic Joint Orientation', fontsize=14)
    ax.set_xlabel('X Direction')
    ax.set_ylabel('Y Direction')
    ax.set_zlabel('Z Direction')

    plt.show()
    
    

# Create rotation matrices for joints from a given matrix type and rotation value
R_01 = RotMatrix('R_01', 'z', 10)
R_12 = RotMatrix('R_12', 'y', 20)
R_23 = RotMatrix('R_23', 'y', 30)
R_34 = RotMatrix('R_34', 'y', 40)
R_45 = RotMatrix('R_45', 'z', 50)

# Calculate rotation matrices relative to the initial robot frame
R_02 = CalculatedRotMatrix('R_02', R_01.matrix, R_12.matrix)
R_03 = CalculatedRotMatrix('R_03', R_02.matrix, R_23.matrix)
R_04 = CalculatedRotMatrix('R_04', R_03.matrix, R_34.matrix)
R_05 = CalculatedRotMatrix('R_05', R_04.matrix, R_45.matrix)
R_05.print_matrix()

# graph the orientation of the joint 5 relative to the initial frame
graph_orientation(R_05)

