import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import random

# Variables for image color modes (used in .convert() in convertToBitmap())
grayscale = "L"
rgb = "RGB"
hsv = "HSV" #Hue, Saturation, Value

#S3 Base URL
baseURL = "https://agro-ai-maize.s3.us-east-2.amazonaws.com/images_compressed/"

class process:

    def convertToBitmap(image_path):
        img = img.resize((64, 64))
        img = Image.open(image_path).convert(rgb)

        return np.array(img, dtype=np.uint8)
    
    def preprocessImages(imgArr):
        imgArr = imgArr.astype('float32') / 255
        #imgArr = np.expand_dims(imgArr, axis=-1)
        #imgArr = np.pad(imgArr, ((0, 0), (2, 2), (2, 2), (0, 0)), 'constant')
        return imgArr
    
    def getURL(imgDict):
        selectedImages = random.sample(list(imgDict.keys()), 64)
        URLs = [baseURL + img for img in selectedImages]
        return URLs

        # fig, axes = plt.subplots(1, len(s3_urls), figsize=(15, 5))

        # for ax, url, img_name in zip(axes, s3_urls, selected_images):
        #     try:
        #         response = requests.get(url)
        #         if response.status_code == 200:
        #             img = Image.open(BytesIO(response.content))
        #             ax.imshow(img)
        #             ax.set_title(img_name, fontsize=8)
        #             ax.axis("off")
        #         else:
        #             ax.set_title("Failed to Load")
        #             ax.axis("off")
        #     except Exception as e:
        #         ax.set_title("Error")
        #         ax.axis("off")
        
        # plt.tight_layout()
        # plt.show()
            



