from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping

import numpy as np
import random

# data creation
def generateData():
  data_x = []
  data_y = []

  for i in range(256):
    # random int sequences
    r = i #random.randint(0, 2**8-1)
    x = list(map(int, list(bin(r)[2:].rjust(8,'0')) ))
    data_x.append(x)

    # one hot encoding
    y = [0]*9
    y[sum(x)] = 1
    data_y.append(y)

  return data_x, data_y


train_x, train_y = generateData()

#create model
model = Sequential()

#get number of columns in training data
n_cols = 8

#add model layers
model.add(Dense(10, activation='relu', input_shape=(n_cols,)))
model.add(Dense(20, activation='relu'))
model.add(Dense(9))

# compile model
model.compile(optimizer='adam', loss='mean_squared_error')

#set early stopping monitor
early_stopping_monitor = EarlyStopping(patience=3)

#train model
model.fit(np.array(train_x), np.array(train_y), epochs=1500)
#, validation_split=0.2)
#, callbacks=[early_stopping_monitor])


# testing
test_x, test_y = generateData()

# for later analysis, save the wrongly predicted
wrong_x = []
wrong_y = []

correct = 0
for testx in test_x:
  pred = model.predict(np.array(testx).reshape(1,8))
  pred_index = list(pred[0]).index(max(pred[0]))

  if pred_index == sum(testx):
    correct += 1
  else: 
    wrong_x.append(testx)
    wrong_y.append(pred)

print("\nEvaluation:")
print("Test: {}/{}".format(correct, len(test_x)))
