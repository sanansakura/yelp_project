from sklearn.model_selection import train_test_split
import keras
from keras import backend
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
import os
import numpy as np
from sklearn import svm
from keras.applications.mobilenet_v2 import MobileNetV2
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.mobilenet_v2 import preprocess_input
from keras.metrics import top_k_categorical_accuracy
from sklearn import preprocessing
from sklearn import linear_model
from keras.regularizers import l2, l1
from sklearn.preprocessing import LabelBinarizer

def one_hot_encoding(y):
    '''
    Convert labels y to one hot encoding.
    '''
    label_binarizer = LabelBinarizer()
    y_one_hot = label_binarizer.fit_transform(y)
    return y_one_hot

def main_mobilenet(Xtrain, ytrain, Xvalid, yvalid, train_batch_size=1000, valid_batch_size=1000, epochs=30):
    '''
    Return a trained model based on the given training set and validation set.
    '''
    train_datagen = ImageDataGenerator(
          width_shift_range=0.2,
          height_shift_range=0.2,
          shear_range=0.2,
          zoom_range=0.2,
          horizontal_flip=True,
          fill_mode='nearest',
          preprocessing_function = preprocess_input)
    train_generator = train_datagen.flow(x = Xtrain, y = ytrain,
                batch_size = train_batch_size,\
                shuffle = False
                )
    valid_datagen = ImageDataGenerator(
                preprocessing_function = preprocess_input)
    valid_generator = valid_datagen.flow(x = Xvalid, y = yvalid,
                batch_size = valid_batch_size,\
                shuffle = False
                )
    mobilenet = MobileNetV2(weights='imagenet', include_top=False, input_shape=(64, 64, 3))
    for layer in mobilenet.layers[:]:
        layer.trainable = True
    model = Sequential()
    model.add(mobilenet)
    model.add(Flatten())
    model.add(Dense(640, activation="relu"))
    model.add(Dropout(0.2))
    model.add(Dense(150, activation="relu"))
    model.add(Dense(15, kernel_regularizer=l2(0.01),
                activity_regularizer=l1(0.01), activation="softmax"))
    model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.RMSprop(lr=1e-4),
              metrics=[top_k_categorical_accuracy])
    history = model.fit_generator(
      train_generator,
      steps_per_epoch=np.ceil(Xtrain.shape[0]/train_batch_size) ,
      epochs=epochs,
      validation_data=valid_generator,
      validation_steps=np.ceil(Xvalid.shape[0]/valid_batch_size),
      verbose=1)
    return model
