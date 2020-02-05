import copy, numpy as np

from input_gen import *

np.random.seed(0)

# compute sigmoid nonlinearity
def sigmoid(x):
    output = 1/(1+np.exp(-x))
    return output

# convert output of sigmoid function to its derivative
def sigmoid_output_to_derivative(output):
    return output*(1-output)

# training dataset generation
binary_dim = 30

data_x = []
data_y = []

'''
for i in range(50):
    tmp = []
    for i in range(31):
        tmp.append(np.random.randint(0,2))

    data_x.append(tmp[:-1].copy())
    data_y.append(tmp[-1])
'''

# sequences = generateInputSequences(binary_dim)
sequences = getGameSequences()

for s in sequences:
    data_x.append(s[:-1].copy())
    data_y.append(s[-1])


# input variables
alpha = 0.1
input_dim = 1
hidden_dim = 32
output_dim = 1


# initialize neural network weights
synapse_0 = 2*np.random.random((input_dim,hidden_dim)) - 1
synapse_1 = 2*np.random.random((hidden_dim,output_dim)) - 1
synapse_h = 2*np.random.random((hidden_dim,hidden_dim)) - 1

synapse_0_update = np.zeros_like(synapse_0)
synapse_1_update = np.zeros_like(synapse_1)
synapse_h_update = np.zeros_like(synapse_h)


# training logic
for j in range(40000):
    
    # get one training sample
    sample_id = np.random.randint(len(sequences))
    a = data_x[sample_id]
    b = data_y[sample_id]
    
    d = 0 # estimate

    overallError = 0
    
    layer_2_deltas = 0
    layer_1_values = list()
    layer_1_values.append(np.zeros(hidden_dim))
    
    # moving along the positions in the binary encoding
    for position in range(binary_dim):
        
        # generate input and output
        X = np.array([a[binary_dim - position - 1]]) # input sequence
        y = np.array([[b]]) # output value

        # hidden layer (input ~+ prev_hidden)
        layer_1 = sigmoid(np.dot(X,synapse_0) + np.dot(layer_1_values[-1],synapse_h))

        # output layer (new binary representation)
        layer_2 = sigmoid(np.dot(layer_1,synapse_1))

        # did we miss?... if so, by how much?
        if position == binary_dim-1: # only calculate Error after last perdiction

            layer_2_error = y - layer_2
            layer_2_deltas = (layer_2_error)*sigmoid_output_to_derivative(layer_2)
            overallError += np.abs(layer_2_error[0])
    
        # decode estimate so we can print it out
        d = int(round(layer_2[0]))
        
        # store hidden layer so we can use it in the next timestep
        layer_1_values.append(copy.deepcopy(layer_1))
    
    future_layer_1_delta = np.zeros(hidden_dim)
    

    # update loop
    for position in range(binary_dim):
        
        X = np.array([[a[position]]])
        layer_1 = layer_1_values[-position-1]
        prev_layer_1 = layer_1_values[-position-2]
        
        # error at output layer
        layer_2_delta = layer_2_deltas
        # error at hidden layer
        layer_1_delta = (future_layer_1_delta.dot(synapse_h.T) + layer_2_delta.dot(synapse_1.T)) * sigmoid_output_to_derivative(layer_1)

        # let's update all our weights so we can try again
        synapse_1_update += np.atleast_2d(layer_1).T.dot(layer_2_delta)
        synapse_h_update += np.atleast_2d(prev_layer_1).T.dot(layer_1_delta)
        synapse_0_update += X.T.dot(layer_1_delta)
        
        future_layer_1_delta = layer_1_delta


    synapse_0 += synapse_0_update * alpha
    synapse_1 += synapse_1_update * alpha
    synapse_h += synapse_h_update * alpha    

    synapse_0_update *= 0
    synapse_1_update *= 0
    synapse_h_update *= 0

    if(j % 1000 == 0) or (j > 36000):
        print("{}".format(j) + "-"*20)
        print("Seq:  " + str("".join([str(t) for t in a])))
        print("Error:" + str(overallError))
        print("Pred: " + str(d))
        print("True: " + str(b))



print("\n\n\n")

# validation phase
validation = getGameValidationSeqs()
val_x = []
val_y = []

for v in validation:
    val_x.append(v[:-1].copy())
    val_y.append(v[-1])

# statistics counter
total = 0
wrong = 0

for i in range(len(validation)):
    a = val_x[i]
    b = val_y[i]
    d = 0 # estimate

    for position in range(binary_dim):
        
        # generate input and output
        X = np.array([a[binary_dim - position - 1]]) # input sequence
        y = np.array([[b]]) # output value

        # feed into network
        layer_1 = sigmoid(np.dot(X,synapse_0) + np.dot(layer_1_values[-1],synapse_h))
        layer_2 = sigmoid(np.dot(layer_1,synapse_1))

        # take prediction of last output
        d = int(round(layer_2[0]))

    # print out progress
    total += 1
    if b != d:
        wrong += 1

print("False to Total predictions: {}/{} - {}\%".format(wrong, total, (wrong/total)*100))
