import os

IMAGE_URL = "https://agro-ai-maize.s3.us-east-2.amazonaws.com/images_compressed/"
RETRAIN_MODEL = True
WEIGHT_PATH = os.path.join(os.path.dirname(__file__), 'app_cache', 'model.weights.h5')

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or 'you-will-never-guess'