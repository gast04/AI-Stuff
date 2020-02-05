import tensorflow as tf
import numpy as np
import random

# Create 200 training sample sequences
train_x = np.zeros((100,200))
train_y = np.zeros((100,1))

for i in range(100):
  for k in range(201): 

    if k == 200:
      train_y[i][0] = random.randint(0,1)
    else:
      train_x[i][k] = random.randint(0,1)


# create 20 validation sequences
val_x = np.zeros((20,200))
val_y = np.zeros((20,1))
for i in range(20):
  for k in range(201): 

    if k == 200:
      val_y[i][0] = random.randint(0,1)
    else:
      val_x[i][k] = random.randint(0,1)

################ caching

BATCH_SIZE = 10
BUFFER_SIZE = 10000


train_x = np.reshape(train_x, (train_x.shape[0], 1, train_x.shape[1]))
train_y = np.reshape(train_y, (train_y.shape[0], 1, train_y.shape[1]))

val_x = np.reshape(val_x, (val_x.shape[0], 1, val_x.shape[1]))
val_y = np.reshape(val_y, (val_y.shape[0], 1, val_y.shape[1]))


train_univariate = tf.data.Dataset.from_tensor_slices((train_x, train_y))
train_univariate = train_univariate.cache().shuffle(BUFFER_SIZE).batch(BATCH_SIZE).repeat()

val_univariate = tf.data.Dataset.from_tensor_slices((val_x, val_y))
val_univariate = val_univariate.batch(BATCH_SIZE).repeat()


# build LSTM-Model
simple_lstm_model = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(8, input_shape=(1,200)),
    #tf.keras.layers.LSTM(8),
    tf.keras.layers.Dense(1)
])

simple_lstm_model.compile(optimizer='adam', loss='mae')

for x, y in val_univariate.take(1):
    print(simple_lstm_model.predict(x,steps=50).shape)



