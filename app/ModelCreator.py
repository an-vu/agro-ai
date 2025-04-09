import keras

def createCNNModel():

    inputLayer = keras.Input(shape=(256, 256, 3))
    x = keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same')(inputLayer)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.MaxPooling2D((2, 2))(x)
    x = keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.MaxPooling2D((2, 2))(x)
    x = keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.MaxPooling2D((2, 2))(x)
    x = keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same', name="attention_layer")(x)
    x = keras.layers.GlobalAveragePooling2D()(x)
    x = keras.layers.Dense(128, activation='relu')(x)
    x = keras.layers.Dropout(0.5)(x)
    
    output = keras.layers.Dense(1, activation='sigmoid')(x)

    return keras.Model(inputs=inputLayer, outputs=output)

def createMLModel():
    # this can be modified freely to create whatever model you'd like.
    # return a keras model to maintain modularity

    inputLayer = keras.Input(shape=(256, 256, 3))
    x = keras.layers.Conv2D()(x) # etc... see structure above

    # fill with desired layers

    outputLayer = keras.layers.Dense(1, activation='sigmoid')(x)

    return keras.Model(inputs=inputLayer, outputs=outputLayer)