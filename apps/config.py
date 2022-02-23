# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from decouple import config
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient, BlobClient

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
        config('DB_ENGINE', default='postgresql'),
        config('DB_USERNAME', default='appseed'),
        config('DB_PASS', default='pass'),
        config('DB_HOST', default='postgres'),
        config('DB_PORT', default=5432),
        config('DB_NAME', default='appseed-flask')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class AzureConfig():
    blob_storage_connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(blob_storage_connect_str)



# Load all possible configurations
config_dict = {
    'Development': Config
}
