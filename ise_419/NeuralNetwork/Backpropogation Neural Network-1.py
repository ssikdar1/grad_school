#######################################################################################
# Back Propagation Neural Networks
# Shan Sikdar <shan.sikdar@gmail.com>
########################################################################################

import math
import random

# Global Constants

EPOCHS = 20000                  #Number of Epochs
LR = 0.3                        #Learning Rate

NI = 3                          #Number of Input Nodes
NH = 2                          #Number of Hidden Nodes
NO = 1                          #Number of Output Nodes

#Information about the data set
SAMPLE_DATA ="firedata.csv"     #Data set
TOTAL_SAMPLE = 517              #Number of examples in the data set
NUM_COL = 4

#Number of examples in the training set (2/3 of data set)
TRAINING_SET = int(TOTAL_SAMPLE - TOTAL_SAMPLE/3)

FIELD_SEPERATOR =","            #Used to get numbers that are seperated by ","

funcName = "SIGMOID"            #Used to choose what activation function you want to use
                                # "SIGMOID" for sigmoid or "HYPER" for hyperbolic tangent

#########################################################################################
#       Activation Functions: sigmoid and Hyperbolic Tangent                            
#########################################################################################

def activeFunc_sig(t):          
    a = 1/(1 + math.exp(-t))
    return a

def activeFunc_hyper(t):
    a = math.tanh(t)
    return a


def activeFunc(funcName,t):
    if funcName == "SIGMOID":
        val = activeFunc_sig(t)
        return val
    elif funcName == "HYPER":
        val = activeFunc_hyper(t)
        return val
    else:
        val = activeFunc_sig(t)
        return val

def dsigmoid(x):
    return 1.0 - x ** 2
  
########################################################################################
# Creating Needed Arrays and Matrices Needed for the  Neural Network                   
########################################################################################
        
def creatingMatrix():
    #Create random wieghts using unformly distributed numbers from 0 to 1
    w1 = [[random.uniform(0.0,1.0)for j in range(NI)] for i in range(NH + 1)]   #+1 for the bias node
    w2 = [[random.uniform(0.0,1.0)for j in range(NH+1)] for i in range(NO + 1)]

    #temp_w1 = [[random.uniform(0.0,1.0)for j in range(NI)] for i in range(NH + 1)]   #+1 for the bias node
    #temp_w2 = [[random.uniform(0.0,1.0)for j in range(NH+1)] for i in range(NO + 1)]


    #the activation nodes for the inputs, hidden, and outputs
    a0 = [0.0 for j in range(NI + 1)]           # +1 for the bias in the input and hidden layers
    a1 = [0.0 for j in range(NH + 1)]
    a2 = [0.0 for j in range(NO+1)]

    #x is the matrix of input values and y is the matrix of output values
    x = [[0.0 for j in range(NI)] for i in range(TOTAL_SAMPLE) ]  
    y = [[0.0 for j in range(NO)] for i in range(TOTAL_SAMPLE) ] 
    
    return (w1,w2,a0,a1,a2,x,y)

########################################################################################
# Initialize the Partial Accumulators       
########################################################################################
   
def initializePartialAccumulators():
    #Partial Accumulators                                   #Partial Accumulators need to be the same dimensions 
    c1 = [[0.0 for j in range(NI)] for i in range(NH+1)]    #as the weight matrix because they exist to change the weight
    c2 = [[0.0 for j in range(NH+1)] for i in range(NO+1)]    #matrix

    return c1,c2
    

########################################################################################
# Forward Propagation       
########################################################################################
def fowardPropogate(w1,w2,a0,a1,a2,funcName,o_file):
    for k in range(NH):
        s = 0
        for i in range(NI):
            s += w1[k+1][i]*a0[i]                 #Linear Basis Function
        a1[k+1] = activeFunc(funcName,s)           
    for j in range(NO):
        s = 0
        for k in range(NH):
            s += w2[j+1][k]*a1[k]
        a2[j+1] = activeFunc(funcName,s)

    return (a1,a2)

########################################################################################
# Backward Propagation       
########################################################################################

def backwardPropogate(w1,w2,a0,a1,a2,y,r,c1,c2,o_file):
    
    d2 = [0.0 for j in range(NO+1)] 
    d1 = [0.0 for j in range(NH+1)]
  
    # calculate error terms for output
    errorDelta = 0.0
    
    for j in range(NO):
        errorDelta = a2[j+1] - y[r][j]
        d2[j+1] = errorDelta * a2[j+1]*(1-a2[j+1])

    # update output weights
    for j in range(NO):
        for k in range(NH):
            c2[j+1][k] += d2[j+1]*a1[k]

    # calculate error terms for hidden        
    for k in range(NH):
        s = 0.0
        for j in range(NO):
            s += w2[j+1][k+1]*d2[j+1]
        d1[k+1] = s*a1[k+1]*(1-a1[k+1])    

    # update input weights
    for k in range(NH):
        for i in range(NI):
            c1[k+1][i] += d1[k+1]*a0[i]
    return c1, c2

########################################################################################
# Train the neural network       
########################################################################################

def train(w1,w2,a0,a1,a2,x,y,funcName,o_file):

    #Initialize Partial Accumulators
    c1,c2 = initializePartialAccumulators()
    
    #Begin Training
    for dataRow in range(TRAINING_SET):
        #read in example from the file
        for i in range(NI):
            a0[i+1] = x[dataRow][i]
        a0[0] = 1.0
        a1[0] = 1.0
        
        #Foward propogate
        a1,a2 = fowardPropogate(w1,w2,a0,a1,a2,funcName,o_file)
        #Backward propogate
        c1,c2 = backwardPropogate(w1,w2,a0,a1,a2,y,dataRow,c1,c2,o_file)
        
    # update Input Weight
    for k in range(NH):
        for i in range(NI):
            w1[k+1][i] -= LR*c1[k+1][i]
    # update Output Weights        
    for j in range(NO):
        for k in range(NH):
            w2[j+1][k] -= LR*c2[j+1][k]
    
    return w1,w2
########################################################################################
# DataValidation - Validate the data       
########################################################################################

def datavalidation(w1,w2,x,y,a0,a1,a2,funcName,o_file):
    totalError = 0.0
    for r in range(TRAINING_SET,TOTAL_SAMPLE):
        for j in range(NI):
            a0[j+1] = x[r][j]
        a0[0] = 1.0
        a1[0] = 1.0
        
        a1,a2 = fowardPropogate(w1,w2,a0,a1,a2,funcName,o_file)
        for j in range(NO):
            predictedValue = a2[j+1]
            error = ((predictedValue - y[r][j])**2)/2
            totalError +=error
            
        overallError = totalError/(TOTAL_SAMPLE-TRAINING_SET)
        
    return overallError

########################################################################################
# write the array to a file
########################################################################################


def write_array_file(o_file,arrayName, A,I,J,Base):
    o_file.write(arrayName+" (Base "+str(Base)+"):\n")
    for j in range(J):
        if (Base == 1 and j == 0):
            continue
        o_file.write("\t[")
        for i in range(I):
            if (i == I-1):
                o_file.write(str(A[j][i]))
            else:
                o_file.write(str(A[j][i])+FIELD_SEPERATOR+" ")
        o_file.write("]\n")
        
    
########################################################################################
# read the file and populate the array for the sample data matrix
########################################################################################
def read_input_file (filename, A, I, J):                    
    r_file = open(filename,'r')
    for j in range(J):
        line = r_file.readline()
        if (line.startswith("#")):
            continue
        line = line.rstrip('\n')
        listnum = line.strip().split(FIELD_SEPERATOR)
        #print( listnum )       
        for i in range(I):
            A[j][i] = float(listnum[i])
           
    r_file.close()
    return A

########################################################################################
# Write input Parameters to the output file
########################################################################################
def write_input_parameters(o_file):
    o_file.write("\nINPUT to Neural Network\n")
    o_file.write("=========================\n")
    o_file.write("Number Of input node = "+ str(NI)+'\n')
    o_file.write("Number Of output node = "+str(NO)+'\n')
    o_file.write("Number Of hidden nodes = "+str(NH)+'\n')
    o_file.write("SAMPLE DATA: \n")
    o_file.write("      Input file name : "+SAMPLE_DATA+"\n")
    o_file.write("      Number of data column :"+str(NUM_COL)+"\n")
    o_file.write("      Number of data rows (TOTAL SAMPLE SIZE) :"+str(TOTAL_SAMPLE)+"\n")
    o_file.write("      Number of data rows for training(TRAINING SIZE):"+ str(TRAINING_SET)+"\n")
    o_file.write("Number Of EPOCHS = "+str(EPOCHS)+'\n')
    o_file.write("Learning Rate = "+str(LR)+'\n')
    o_file.write("Activation Function used: " +funcName+'\n')
    o_file.write("-------------------------------------------------------------------------------")
    o_file.write("\n\n\nOuput of the RUN\n")

########################################################################################
# Read the datafile and populate x and y
########################################################################################
def read_datafile (x,y):
    # Initializing the data matrix
    sampledata = [[0.0 for j in range(NI+NO)] for i in range(TOTAL_SAMPLE)]

    # Read the sample data from a text file and populate the x and y matrix
    # Preprocess the output data while reading into the y matrix                 
    sampledata = read_input_file(SAMPLE_DATA,sampledata,NUM_COL,TOTAL_SAMPLE)
    for i in range(TOTAL_SAMPLE):                       #i is the number of examples
        for j in range(NI+NO):                          #j number of columns
            if (j < NI):                                #the input columns
                x[i][j] = sampledata[i][j]
            else:
                y[i][j-NI] = sampledata[i][j]               
    return x,y

########################################################################################
# Normalize the input data - X[i] - min/ max - min ,  Y[i] -min / max-min
########################################################################################


def preprocess_inputdata(x,y):
    min_max = [[0.0 for j in range(2)] for i in range(NI+NO)]
    
    for j in range(TOTAL_SAMPLE):
        for i in range(NI+NO):
            if (i < NI):
                #print("j="+str(j)+" i="+str(i))
                if (x[j][i] < min_max[i][0]):           # 0 element is min
                    min_max[i][0] = x[j][i]
                if (x[j][i] > min_max[i][1]):           # 1 element is max
                    min_max[i][1] = x[j][i]
            else:
                if (y[j][i-NI] < min_max[i][0]):        # 0 element is min
                    min_max[i][0] = y[j][i-NI]
                if (y[j][i-NI] > min_max[i][1]):        # 1 element is max
                    min_max[i][1] = y[j][i-NI]
              
    
    for i in range(TOTAL_SAMPLE):
        for j in range(NI+NO):
            if ( j < NI):
                x[i][j] = (x[i][j] - min_max[j][0]) / (min_max[j][1] - min_max[j][0])
            else:
                y[i][j-NI] = (y[i][j-NI] - min_max[j][0]) / (min_max[j][1] - min_max[j][0])
    return x,y


def main():
    
    # Open Output file to record the Result        
    o_file = open("RunResult.txt",'w')
    write_input_parameters(o_file)
    
    if ((NI + NO) <= NUM_COL) :
       # Create Matrix for the weights, activation and for reading input and output data
        w1,w2,a0,a1,a2,x,y = creatingMatrix()
        # Read the data from input file and assign to x and y
        x, y = read_datafile(x,y)
        # Preprocess the input data
        x,y = preprocess_inputdata(x,y)
        
        o_file.write("Random Weights before training\n")
        write_array_file(o_file,"w1",w1,NI,NH+1,1)
        o_file.write("\n")
        write_array_file(o_file,"w2",w2,NH+1,NO+1,1)
        o_file.write("\n")
        o_file.write(">>>>>>>>>>>>>>>> Training Started <<<<<<<<<<<<<<<<<<<\n")

        lasterror = 100
        o_file.write("EPOCH \t OverallError\n");
        o_file.write("===== \t ============\n");
        for t in range(EPOCHS):
            # Training Phase
            w1,w2 = train(w1,w2,a0,a1,a2,x,y,funcName,o_file)
            
            # Validation Phase            
            overallError = datavalidation(w1,w2,x,y,a0,a1,a2,funcName,o_file)        
            
            #o_file.write("EPOCH ="+str(t)+ " OverallError="+str(overallError)+"\n");
            o_file.write(str(t)+ " \t "+str(overallError)+"\n");
            
            if overallError > lasterror:
##                o_file.write(" Output Weights\n")
##                write_array_file(o_file,"w1",w1,NI,NH+1,1)
##                write_array_file(o_file,"w2",w2,NH+1,NO+1,1)
                break
            else:
                lasterror = overallError
            
           
        o_file.write("\n\nFinal Output Weights\n")
        write_array_file(o_file,"w1",w1,NI,NH+1,1)
        o_file.write("\n")
        write_array_file(o_file,"w2",w2,NH+1,NO+1,1)
        o_file.write("\n")
        o_file.write("Overall Error = "+ str(overallError)+'\n')

        
    else:
        print ("Number of column in datafile is less than number of input & number of output")
        o_file.write ("Number of column in datafile is less than number of input & number of output\n")        

    # Close the output file
    o_file.close()
main()    
    

