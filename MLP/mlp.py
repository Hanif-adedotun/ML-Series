import numpy as np
import copy
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score


# Step 1: Data Preparation
# Load Iris dataset
iris = load_iris()
X = iris.data
y = iris.target.reshape(-1,1)
# Preprocessing if necessary (no preprocessing needed for Iris dataset)

def one_hot_encode(y):
     maps = {0: [1., 0., 0.], 1: [0., 1., 0.], 2: [0., 0., 1.]}
     new_y = []
     for i in y:
        new_y.append(maps[i[0]])
     return np.array(new_y)

# Step 2: Define activation functions
def relu(x):
  return np.maximum(0, x)

def softmax(x):
    e_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return e_x / np.sum(e_x, axis=1, keepdims=True)

# Define derivative of activation function (ReLU derivative)
def relu_derivative(x):
  return np.where(x > 0, 1, 0)

y_onehot = one_hot_encode(y)
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_onehot, test_size=0.2, random_state=42)

# Step 3: Initialize weights and biases
def initialize_parameters(hidden_size, hidden_size2):
     # Define the network architecture
     input_size = X_train.shape[1]  # 4 features
     output_size = y_train.shape[1]  # 3 unique labels

     # Initialize weights and biases
     np.random.seed(42)
     weights = {
     'h1': np.random.uniform(-0.1, 0.1, (input_size, hidden_size)),
     'h2': np.random.uniform(-0.1, 0.1, (hidden_size, hidden_size2)),
     'out': np.random.uniform(-0.1, 0.1, (hidden_size2, output_size))
     }
     biases = {
     'h1': np.random.uniform(-0.1, 0.1, hidden_size),
     'h2': np.random.uniform(-0.1, 0.1, hidden_size2),
     'out': np.random.uniform(-0.1, 0.1, output_size)
     }
     return weights, biases
 
# Step 4: Forward propagation
def forward(X, weights, biases):
    z1 = np.dot(X, weights['h1']) + biases['h1'] # W1.X + b1
    a1 = relu(z1)
    z2 = np.dot(a1, weights['h2']) + biases['h2'] # W2.A1 + b2
    a2 = relu(z2)
    z3 = np.dot(a2, weights['out']) + biases['out'] # Wout.A2 + bout
    a3 = softmax(z3)
    
    return a1, a2, a3

# Step 5: Backward propagation
def backward_propagation(X, y, a1, a2, a3, learning_rate, weights, biases):
    m = y.shape[0]
    
    dz3 = a3 - y
    dw3 = np.dot(a2.T, dz3) / m
    print(dw3.shape)

    db3 = np.sum(dz3, axis=0) / m

    dz2 = np.dot(dz3, weights['out'].T) * relu_derivative(a2)
    dw2 = np.dot(a1.T, dz2) / m
    db2 = np.sum(dz2, axis=0) / m

    dz1 = np.dot(dz2, weights['h2'].T) * relu_derivative(a1)
    dw1 = np.dot(X.T, dz1) / m
    db1 = np.sum(dz1, axis=0) / m

    # Update weights and biases
    weights['h1'] -= learning_rate * dw1
    weights['h2'] -= learning_rate * dw2
    weights['out'] -= learning_rate * dw3
    biases['h1'] -= learning_rate * db1
    biases['h2'] -= learning_rate * db2
    biases['out'] -= learning_rate * db3
    
    
# Step 6: train the neural network
def train_mlp(hidden_layer_size, hidden_layer_size2, epochs, learning_rate):
     scores_so_far = {}
     weights, biases = initialize_parameters(hidden_layer_size, hidden_layer_size2)

     # Training the network
     for epoch in range(epochs):
          a1, a2, a3 = forward(X_train, weights, biases)
          backward_propagation(X_train, y_train, a1, a2, a3, learning_rate, weights, biases)

          predictions = np.argmax(a3, axis=1)
          true_labels = np.argmax(y_train, axis=1)

          curr_accuracy = accuracy_score(true_labels, predictions)

          print(f'Accuracy: {curr_accuracy}, epoch: {epoch}')

          
          scores_so_far[curr_accuracy] = [copy.deepcopy(weights), copy.deepcopy(biases), copy.deepcopy(a3)]
               
     # Evaluate the model
     weights_new = scores_so_far[max(scores_so_far.keys())][0]
     biases_new = scores_so_far[max(scores_so_far.keys())][1]    

     _, _, out_test = forward(X_test, weights_new, biases_new)
     # print()

     y_pred_train = np.argmax(scores_so_far[max(scores_so_far.keys())][2], axis=1)
     train_labels = np.argmax(y_train, axis=1)

     accuracy = accuracy_score(train_labels, y_pred_train)

     print(f'Model Train Accuracy: {accuracy * 100:.2f}')

     y_pred = np.argmax(out_test, axis=1)
     test_labels = np.argmax(y_test, axis=1)

     accuracy = accuracy_score(test_labels, y_pred)

     print(f'Model Test Accuracy: {accuracy * 100:.2f}')
     
     return weights, biases
     
# Call the function to train Neural Nework
weights, biases = train_mlp(hidden_layer_size=90, hidden_layer_size2=55, epochs=200, learning_rate=0.1)


def predict(X):     
     _, _, prediction = forward(X, weights, biases)
     predictions = (prediction > 0.5).astype(int)
     return predictions

predictions = predict(X_test)