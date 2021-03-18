from tensorflow.keras.layers import Conv2D, BatchNormalization, Activation, \
    UpSampling2D, Add, Concatenate, MaxPool2D
from tensorflow.keras import Input
from tensorflow.keras.models import Model
import tensorflow as tf
import tensorflow.keras.backend as K
from tensorflow.keras.losses import binary_crossentropy

from utils.BaseModel import BaseModel

epsilon = 1e-5
smooth = 1


def tversky(y_true, y_pred):
    y_true_pos = K.flatten(y_true)
    y_pred_pos = K.flatten(y_pred)
    true_pos = K.sum(y_true_pos * y_pred_pos)
    false_neg = K.sum(y_true_pos * (1 - y_pred_pos))
    false_pos = K.sum((1 - y_true_pos) * y_pred_pos)
    alpha = 0.7
    return (true_pos + smooth) / (true_pos + alpha * false_neg + (1 - alpha) * false_pos + smooth)


def focal_tversky(y_true, y_pred):
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)

    pt_1 = tversky(y_true, y_pred)
    gamma = 0.75
    return K.pow((1 - pt_1), gamma)


def tversky_loss(y_true, y_pred):
    return 1 - tversky(y_true, y_pred)


class ResUnet(BaseModel):
    def __resblock(self, X, f):
        '''
        function for creating res block
        '''
        X_copy = X  # copy of input

        # main path
        X = Conv2D(f, kernel_size=(1, 1), kernel_initializer='he_normal')(X)
        X = BatchNormalization()(X)
        X = Activation('relu')(X)

        X = Conv2D(f, kernel_size=(3, 3), padding='same', kernel_initializer='he_normal')(X)
        X = BatchNormalization()(X)

        # shortcut path
        X_copy = Conv2D(f, kernel_size=(1, 1), kernel_initializer='he_normal')(X_copy)
        X_copy = BatchNormalization()(X_copy)

        # Adding the output from main path and short path together
        X = Add()([X, X_copy])
        X = Activation('relu')(X)

        return X

    def __upsample_concat(self, x, skip):
        '''
        funtion for upsampling image
        '''
        X = UpSampling2D((2, 2))(x)
        merge = Concatenate()([X, skip])

        return merge

    def get_model(self):
        input_shape = (256, 256, 3)
        X_input = Input(input_shape)  # iniating tensor of input shape

        # Stage 1
        conv_1 = Conv2D(16, 3, activation='relu', padding='same', kernel_initializer='he_normal')(X_input)
        conv_1 = BatchNormalization()(conv_1)
        conv_1 = Conv2D(16, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv_1)
        conv_1 = BatchNormalization()(conv_1)
        pool_1 = MaxPool2D((2, 2))(conv_1)

        # stage 2
        conv_2 = self.__resblock(pool_1, 32)
        pool_2 = MaxPool2D((2, 2))(conv_2)

        # Stage 3
        conv_3 = self.__resblock(pool_2, 64)
        pool_3 = MaxPool2D((2, 2))(conv_3)

        # Stage 4
        conv_4 = self.__resblock(pool_3, 128)
        pool_4 = MaxPool2D((2, 2))(conv_4)

        # Stage 5 (bottle neck)
        conv_5 = self.__resblock(pool_4, 256)

        # Upsample Stage 1
        up_1 = self.__upsample_concat(conv_5, conv_4)
        up_1 = self.__resblock(up_1, 128)

        # Upsample Stage 2
        up_2 = self.__upsample_concat(up_1, conv_3)
        up_2 = self.__resblock(up_2, 64)

        # Upsample Stage 3
        up_3 = self.__upsample_concat(up_2, conv_2)
        up_3 = self.__resblock(up_3, 32)

        # Upsample Stage 4
        up_4 = self.__upsample_concat(up_3, conv_1)
        up_4 = self.__resblock(up_4, 16)

        # final output
        out = Conv2D(1, (1, 1), kernel_initializer='he_normal', padding='same', activation='sigmoid')(up_4)

        seg_model = Model(X_input, out)
        adam = tf.keras.optimizers.Adam(lr=0.05, epsilon=0.1)
        seg_model.compile(optimizer=adam,
                          loss=focal_tversky,
                          metrics=[tversky]
                          )

        return seg_model