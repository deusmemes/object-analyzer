from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras import Input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, Flatten, AveragePooling2D

from utils.BaseModel import BaseModel


class Classifier(BaseModel):
    def __init__(self):
        pass

    def get_model(self):
        clf_model = ResNet50(weights='imagenet', include_top=False, input_tensor=Input(shape=(256, 256, 3)))
        for layer in clf_model.layers:
            layer.trainable = False

        head = clf_model.output
        head = AveragePooling2D(pool_size=(4, 4))(head)
        head = Flatten(name='Flatten')(head)
        head = Dense(256, activation='relu')(head)
        head = Dropout(0.3)(head)
        head = Dense(256, activation='relu')(head)
        head = Dropout(0.3)(head)
        head = Dense(2, activation='softmax')(head)

        model = Model(clf_model.input, head)
        model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=["accuracy"]
                      )

        return model

    def load_model(self):
        pass

    def save_model(self, model):
        model.save('classifier.json')
        model.save_weights('classifier_weights.hdf5')