import os

IMAGE_URL = "https://agro-ai-maize.s3.us-east-2.amazonaws.com/images_compressed/"

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'