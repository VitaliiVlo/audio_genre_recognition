import warnings

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

warnings.filterwarnings('ignore')

# seed
seed_value = 128
import os

os.environ['PYTHONHASHSEED'] = str(seed_value)
import random

random.seed(seed_value)
np.random.seed(seed_value)

data = pd.read_csv('v2/df_features2_test.csv')

genre_list = data.iloc[:, 0]
encoder = LabelEncoder()
y = encoder.fit_transform(genre_list)

X = np.array(data.iloc[:, 1:], dtype=float)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True, random_state=seed_value)

# normalization
std_scale = StandardScaler().fit(X_train)
X_train = std_scale.transform(X_train)
X_test = std_scale.transform(X_test)

from keras import models
from keras import layers

model = models.Sequential()
model.add(layers.Dense(256, activation='relu', input_shape=(X_train.shape[1],)))

model.add(layers.Dropout(0.2))

model.add(layers.BatchNormalization())

model.add(layers.Dense(128, activation='relu'))

model.add(layers.Dropout(0.2))

model.add(layers.BatchNormalization())

model.add(layers.Dense(64, activation='relu'))

model.add(layers.Dropout(0.5))

model.add(layers.Dense(10, activation='softmax'))

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(X_train,
                    y_train,
                    epochs=60,
                    batch_size=128)

test_loss, test_acc = model.evaluate(X_test, y_test)
print(test_acc)

from sklearn.externals import joblib

model.save('model.h5')
joblib.dump(std_scale, 'scale.save')
joblib.dump(encoder, 'encoder.save')

import pydot
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
from keras.utils import plot_model
plot_model(model, to_file='model.png', show_shapes=True, show_layer_names=True)
