import os
import io
import json
from tkinter import END
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeatureTypes
import requests
#from PIL import Image, IMageDraw, ImageFont

#Init client
credentials = json.load(open('.\\app\\azure\credentials.json'))
API_KEY = credentials['API_KEY']
ENDPOINT = credentials['ENDPOINT']
cv_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY)) #Computer vision client instance


image_url = 'https://media.newyorker.com/photos/5bd20ee0f4dc8b77a8156d08/master/pass/FoodNewsletter-Fridge.jpg'

"""
Detect object
Doc: https://westus.dev.cognitive.microsoft.com/docs/services/computer-vision-v3-2/operations/5e0cdeda77a84fcd9a6d4e1b
Azure Python SDK https://docs.microsoft.com/en-us/python/api/overview/azure/cognitiveservices-vision-computervision-readme?view=azure-python
"""
response = cv_client.detect_objects(image_url)
print(response.objects)
for o in response.objects:
    print("Object: {0}".format(o.object_property))
    print("Confidence {0}".format(o.confidence*100))







