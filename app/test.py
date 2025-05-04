from sklearn.model_selection import train_test_split
from PIL import Image
import os, cv2, numpy as np, keras, tensorflow as tf, uuid

def make_gradcam_heatmap(imgArr, model, pred_index=None):
    # Create model mapping input -> attention layer + output
    grad_model = keras.models.Model(
        inputs=model.input,
        outputs=[model.get_layer("attention_layer").output, model.output]
    )

    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(imgArr)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    # Compute gradients
    grads = tape.gradient(class_channel, last_conv_layer_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # Weight the channels by importance
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    # Normalize the heatmap
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()

def save_and_overlay_heatmap(imgName, imgPath, hmpArr, alpha=0.4):
    img = cv2.imread(imgPath)
    img = cv2.resize(img, (256, 256))

    hmpArr = cv2.resize(hmpArr, (img.shape[1], img.shape[0]))
    hmpArr = np.uint8(255 * hmpArr)
    hmpColor = cv2.applyColorMap(hmpArr, cv2.COLORMAP_JET)
    hmpOverlay = cv2.addWeighted(img, 1 - alpha, hmpColor, alpha, 0)

    hmpPath = os.path.join(os.path.dirname(__file__), 'static', 'imgHeatmap', f'heatmap_{imgName}')
    os.makedirs(os.path.dirname(hmpPath), exist_ok=True)
    cv2.imwrite(hmpPath, hmpOverlay)

    return '/' + hmpPath


if __name__ == "__main__":
    imgName = 'DSC00108.JPG'
    imgPath = os.path.join(os.path.dirname(__file__), 'static', 'imgHandheld', imgName)

    # Preprocess image
    img = Image.open(imgPath).convert('RGB').resize((256, 256))
    imgArr = np.expand_dims(np.array(img, dtype=np.float32) / 255.0, axis=0)

    # Load keras models
    model = keras.models.load_model(os.path.join(os.path.dirname(__file__), 'static', 'model.weights.keras'))
    last_conv_layer_name = 'conv2d_2'

    # Generate heatmap
    hmpArr = make_gradcam_heatmap(imgArr, model)
    hmpPath = save_and_overlay_heatmap(imgName, imgPath, hmpArr)

    print('original', imgPath, 'heatmap', hmpPath)