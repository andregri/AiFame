# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from decouple import config
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

class Config(object):
    load_dotenv()

    basedir = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config('DB_ENGINE', default=os.getenv('DB_ENGINE')),
        config('DB_USERNAME', default=os.getenv('DB_USERNAME')),
        config('DB_PASS', default=os.getenv('DB_PASS')),
        config('DB_HOST', default=os.getenv('DB_HOST')),
        config('DB_PORT', default=os.getenv('DB_PORT')),
        config('DB_NAME', default=os.getenv('DB_NAME'))
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class AzureConfig():
    blob_storage_connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(blob_storage_connect_str)

    # Create ComputerVisionClient object
    computervision_endpoint = os.getenv('AZURE_CV_ENDPOINT')
    computervision_apikey = os.getenv('AZURE_CV_APIKEY')
    computervision_client = ComputerVisionClient(
        computervision_endpoint,
        CognitiveServicesCredentials(computervision_apikey)
    )

# Load all possible configurations
config_dict = {
    'Development': Config
}
