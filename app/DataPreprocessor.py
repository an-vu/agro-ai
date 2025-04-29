import numpy as np, pandas as pd, matplotlib.pyplot as plt, os, time, keras, random
from app import ModelCreator
from sklearn.model_selection import train_test_split
from PIL import Image
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def getAnnotations():
    path = os.path.join(os.path.dirname(__file__), 'static', 'imgAnnotations.csv')

    if not os.path.exists(path):
        print(f'Error: {path} not found.')
        return None

    return pd.read_csv(path, index_col=0)
    
def arrangeAnnotations(df):
    results = []
    prev = None

    for index, row in df.iterrows():        
        if index == prev:
            continue
        prev = index

        if all(row.iloc[:4] == '0'):
            results.append((index, 0))
        else:
            results.append((index, 1))

    return pd.DataFrame(results, columns=['Image', 'Label'])

def getImages(imgNames = None):
    path = os.path.join(os.path.dirname(__file__), 'static', 'imgHandheld')
    imgMaps = []
    imgNames = [] if imgNames == None else imgNames

    for imgName in os.listdir(path):
        imgPath = os.path.join(path, imgName)

        # Open image, convert to RGB, resize to 256x256
        img = Image.open(imgPath).convert('RGB').resize((256, 256))

        # Convert to NumPy array and normalize (0-255 -> 0-1)
        imgArr = np.array(img, dtype=np.float32) / 255.0

        # Ensure shape is (256, 256, 3) for RGB
        imgMaps.append(imgArr)
        imgNames.append(imgName)

    return np.array(imgMaps), imgNames  # Return all images as a NumPy array

def getSingleImage(imgName = None):
    path = os.path.join(os.path.dirname(__file__), 'static', 'imgHandheld')
    imgName = random.choice(os.listdir(path)) if imgName == None else imgName
    imgPath = os.path.join(path, imgName)
    img = Image.open(imgPath).convert('RGB').resize((256, 256))
    imgArr = [np.array(img, dtype=np.float32) / 255.0]

    return np.array(imgArr), imgName

def preprocessData(testSize=0.2, randomSeed=int(time.time())):
    # Returns xTrain, yTrain, xTest, yTest
    
    df = getAnnotations()
    if df is None:
        return (None, None), (None, None)

    dfLabels = arrangeAnnotations(df)
    imgMaps, imgNames = getImages()

    matchedImages = []
    matchedLabels = []

    for imgName, img in zip(imgNames, imgMaps):
        labelRow = dfLabels[dfLabels['Image'] == imgName]
        if not labelRow.empty:
            matchedImages.append(img)  
            matchedLabels.append(int(labelRow.iloc[0]['Label']))

    matchedImages = np.array(matchedImages)
    matchedLabels = np.array(matchedLabels)

    xTrain, xTest, yTrain, yTest = train_test_split(matchedImages, matchedLabels, test_size=testSize, random_state=randomSeed)

    # **Define Data Augmentation**
    datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=25,
        zoom_range=0.2,
        width_shift_range=0.1,
        height_shift_range=0.1,
        brightness_range=[0.8,1.2],
        horizontal_flip=True,
        fill_mode='nearest'
    )

    # Create an augmented data generator
    train_generator = datagen.flow(xTrain, yTrain, batch_size=24)

    return train_generator, (xTest, yTest)