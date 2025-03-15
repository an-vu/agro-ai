import keras

def createCNNModel():
    # this is a binary-modified LeNet-5 CNN model using Keras API

    inputLayer = keras.Input(shape=(256, 256, 3))
    x = keras.layers.Conv2D(6, kernel_size=(5,5), strides=(1,1), activation='tanh', padding='same')(inputLayer)
    x = keras.layers.AveragePooling2D(pool_size=(2,2), strides=(2,2), padding='valid')(x)
    x = keras.layers.Conv2D(16, kernel_size=(5,5), strides=(1,1), activation='tanh', padding='valid')(x)
    x = keras.layers.AveragePooling2D(pool_size=(2,2), strides=(2,2), padding='valid')(x)
    x = keras.layers.Conv2D(120, kernel_size=(5,5), strides=(1,1), activation='tanh', padding='valid')(x)
    x = keras.layers.Flatten()(x)
    x = keras.layers.Dense(84, activation='tanh')(x)
    outputLayer = keras.layers.Dense(1, activation='sigmoid')(x)

    return keras.Model(inputs=inputLayer, outputs=outputLayer)

def createMLModel():
    # this can be modified freely to create whatever model you'd like.
    # return a keras model to maintain modularity

    inputLayer = keras.Input(shape=(256, 256, 3))
    x = keras.layers.Conv2D()(x) # etc... see structure above

    # fill with desired layers

    outputLayer = keras.layers.Dense(1, activation='sigmoid')(x)

    return keras.Model(inputs=inputLayer, outputs=outputLayer)