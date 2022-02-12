import tensorflow as tf
import numpy as np
from tensorflow import keras

model = tf.keras.Sequential([
	keras.layers.Dense(units=2, input_shape=(2, )),
	keras.layers.Dense(128, activation=tf.nn.relu),
	keras.layers.Dense(4, activation=tf.nn.softmax)
])

#opt = SGD(lr=0.01, momentum=0.9)

model.compile(optimizer='adam',  loss='sparse_categorical_crossentropy')

xs = np.array([-1.0, -1.2, -1.1, -1.4, -1.0, -1.2, -1.1, -1.4, 1.0, 1.2, 1.1, 1.4,  1.0,  1.2,  1.1,  1.4], dtype=float)
ys = np.array([ 1.0,  1.2,  1.1,  1.4, -1.0, -1.2, -1.1, -1.4, 1.0, 1.2, 1.1, 1.4, -1.0, -1.2, -1.1, -1.4], dtype=float)
lb = np.array([     0,     0,      0,     0,     1,     1,     1,      1,     2,    2,    2,    2,     3,     3,     3,      3])

xxs =np.array( [[xs[i], ys[i]] for i in range(len(xs))], dtype=float)
print(xxs)
#zs = np.array([], dtype=float)
#rs = np.array([], dtype=float)

#xss = np.arange(0.0, 100)
#yss = np.array([3*i+1for i in xss], dtype=float)
#print(yss)

model.fit(xxs,  lb,  epochs=50)

print(model.predict([[-5.123, 3]]))