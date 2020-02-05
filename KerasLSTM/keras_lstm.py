from __future__ import print_function
import collections
import os,sys
import tensorflow as tf
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Embedding, Dropout, TimeDistributed
from keras.layers import LSTM
from keras.optimizers import Adam
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint
import numpy as np
import argparse

from input_gen import *

data_x = []
data_y = []

SEQ_LENGTH = 60
sequences = generateInputSequences(SEQ_LENGTH)
sequences = getGameSequences()

for s in sequences:
    data_x.append(s[:30].copy())
    data_y.append(s[30:60].copy())

num_steps = 30

# model generation
hidden_size = 200
use_dropout=False
model = Sequential()
model.add(LSTM(hidden_size, return_sequences=True))
model.add(LSTM(hidden_size, return_sequences=False))
if use_dropout:
    model.add(Dropout(0.5))
#model.add(TimeDistributed(Dense(vocabulary)))
model.add(Activation('softmax'))
model.add(Dense(1))


optimizer = Adam()
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['categorical_accuracy'])

model.build()

#print(model.summary())
#sys.exit()


resh_x = np.array(data_x).reshape(len(sequences),30,1)
#resh_y = np.array(data_y).reshape(len(sequences),30)

resh_y = np.zeros((len(sequences),1))
for i in range(len(data_y)):
    resh_y[i] = data_y[i][0]

# model training
model.fit(resh_x, resh_y, epochs=1000)

print("\nStart Evaluation")
pred = model.predict(resh_x[1].reshape(1,30,1))
print(resh_x[1])
print(pred, resh_y[1])

pred = model.predict(resh_x[3].reshape(1,30,1))
print(resh_x[3])
print(pred, resh_y[3])




print("\nEnd Of Network")
