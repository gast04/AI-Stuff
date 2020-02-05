from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping

import numpy as np
import pickle

# load sequences
with open('training_sequences.pickle', 'rb') as handle:
    training_set = pickle.load(handle)

train_x = []
train_y = []
for s in training_set:
  train_x.append(s[:-1].copy())
  train_y.append(s[-1])

#create model
model = Sequential()

#get number of columns in training data
n_cols = 200

#add model layers
model.add(Dense(200, activation='relu', input_shape=(n_cols,)))
model.add(Dense(200, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(1))

# compile model
model.compile(optimizer='adam', loss='mean_squared_error')


# reshape data
resh_x = np.array(train_x)
resh_y = np.array(train_y)

#set early stopping monitor, (not used)
early_stopping_monitor = EarlyStopping(patience=3)

#train model
model.fit(resh_x, resh_y, epochs=50)
#, validation_split=0.2)
#, callbacks=[early_stopping_monitor])


# testing
def validate(sequences):
  val_x = []
  val_y = []
  for s in sequences:
    val_x.append(s[:-1].copy())
    val_y.append(s[-1])

  # for later analysis, save the wrongly predicted
  wrong_x = []
  wrong_y = []

  correct = 0
  for i in range(len(val_x)):
    pred = model.predict(np.array(val_x[i]).reshape(1,200))

    if int(round(pred[0][0])) == val_y[i]:
      correct += 1
    else: 
      wrong_x.append(i)
      wrong_y.append(pred)

  print("Evaluation:")
  print("Test: {}/{}".format(correct, len(val_x)))

with open('validation_sequences.pickle', 'rb') as handle:
  validation_set = pickle.load(handle)

with open('test_sequences.pickle', 'rb') as handle:
  test_set = pickle.load(handle)


print("\nuse Validation Set")
validate(validation_set)

print("\nuse Test Set")
validate(test_set)
