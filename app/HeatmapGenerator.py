import matplotlib
matplotlib.use('Agg')
import cv2, keras, os, numpy as np, tensorflow as tf, matplotlib.pyplot as plt
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import DataPreprocessor, ModelCreator, AppConfig

from PIL import Image

def generateHeatmap(model, imgArray, layerName):
    gradModel = tf.keras.models.Model([model.input], [model.get_layer(layerName).output, model.output])

    with tf.GradientTape() as tape:
        convOutputs, predictions = gradModel(imgArray)
        loss = predictions[:, 0]

    gradients = tape.gradient(loss, convOutputs)
    pooledGrads = tf.reduce_mean(gradients, axis=(0, 1, 2))
    convOutputs = convOutputs[0]

    heatmap = tf.reduce_mean(convOutputs * pooledGrads, axis=-1)
    heatmap = np.maximum(heatmap, 0)
    heatmap /= np.max(heatmap)

    return np.array(heatmap)

def overlayHeatmap(imgPath, heatmap, alpha=0.4):
    img = cv2.imread(imgPath)
    img = cv2.resize(img, (256, 256))

    heatmap = cv2.resize(heatmap, (256, 256))
    heatmap = np.uint8(255 * heatmap)
    heatmapColor = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    return cv2.addWeighted(img, 1 - alpha, heatmapColor, alpha, 0)

def showHeatmap():
    train_generator, (xTest, yTest) = DataPreprocessor.preprocessData()
    model = ModelCreator.createCNNModel()

    if not AppConfig.RETRAIN_MODEL and os.path.exists(AppConfig.WEIGHT_PATH):
        model.load_weights(AppConfig.WEIGHT_PATH)
    else:
        model.compile(loss='binary_crossentropy', optimizer='SGD', metrics=['accuracy'])
        model.fit(train_generator, epochs=2, validation_data=(xTest, yTest))
        model.save_weights(AppConfig.WEIGHT_PATH)

    img_path = os.path.join(os.path.dirname(__file__), 'static', 'imgHandheld', 'DSC00108.JPG')
    img = Image.open(img_path).convert('RGB').resize((256, 256))
    img_array = np.expand_dims(np.array(img, dtype=np.float32) / 255.0, axis=0)

    heatmap = generateHeatmap(model, img_array, "conv2d_2")
    overlay_img = overlayHeatmap(img_path, heatmap)

    output_filename = 'heatmap_output.png'
    output_path = os.path.join(os.path.dirname(__file__), 'static', output_filename)

    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.title("Original Image")

    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(overlay_img, cv2.COLOR_BGR2RGB))
    plt.title("Grad-CAM Heatmap")

    plt.savefig(output_path)
    plt.close()

    return output_filename