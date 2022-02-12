import tensorflow as tf
import numpy as np
from tensorflow import keras

model = tf.keras.Sequential([
	keras.layers.Dense(units=1, input_shape=[1]),
	keras.layers.Dense(256),
	keras.layers.Dense(1)
])

#opt = SGD(lr=0.01, momentum=0.9)

model.compile(optimizer='adam', loss='mean_squared_error')

xs = np.array([-1.0, 0.0, 1.0, 2.0, 3.0, 4.0], dtype=float)
ys = np.array([-2.0, 1.0, 4.0, 7.0, 10.0, 13.0], dtype=float)

xss = np.arange(0.0, 100)
yss = np.array([3*i+1for i in xss], dtype=float)
print(yss)

model.fit(xss, yss, epochs=50)

print(model.predict([1000]))