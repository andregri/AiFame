import json
import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from PIL import Image

# Authenticate client
credentials = json.load(open('credentials.json'))
API_KEY = credentials['API_KEY']
ENDPOINT = credentials['ENDPOINT']
computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY)) #Computer vision client instance

# Tag a local image
# Open local image file
images_folder = os.path.join (os.path.dirname(os.path.abspath(__file__)), "images")
local_image_path = os.path.join (images_folder, "foods.jpg")
local_image = open(local_image_path, "rb")

# Call API local image
detect_objects_results_local = computervision_client.detect_objects_in_stream(local_image)

original_image = Image.open(local_image_path)

# Print results of detection with bounding boxes
print("Detecting objects in local image:")
if len(detect_objects_results_local.objects) == 0:
    print("No objects detected.")
else:
    for n, object in enumerate(detect_objects_results_local.objects):
        print("{} with confidence {} at location {}, {}, {}, {}".format( \
        object.object_property, object.confidence, \
        object.rectangle.x, object.rectangle.x + object.rectangle.w, \
        object.rectangle.y, object.rectangle.y + object.rectangle.h))

        if object.object_property == 'Food' or object.object_property == 'Fruit':
            # Save cropped image
            left = object.rectangle.x
            right = object.rectangle.x + object.rectangle.w
            top = object.rectangle.y
            bottom = object.rectangle.y + object.rectangle.h
            cropped_image = original_image.crop((left, top, right, bottom))
            cropped_image_path = os.path.join(images_folder, f"{n}.jpg")
            cropped_image.save(cropped_image_path, "JPEG")

            # re-open the cropped image as a binary file because azure library doesn't like PIL image object
            cropped_image = open(cropped_image_path, "rb")

            # Describe cropped image
            description_result = computervision_client.describe_image_in_stream(cropped_image)

            # Get the captions (descriptions) from the response, with confidence level
            print("--Description of local image: ")
            if (len(description_result.captions) == 0):
                print("----No description detected.")
            else:
                for caption in description_result.captions:
                    print("----'{}' with confidence {:.2f}%".format(caption.text, caption.confidence * 100))
            print()

            # Tag cropped image
            cropped_image = open(cropped_image_path, "rb")
            tags_result_local = computervision_client.tag_image_in_stream(cropped_image)

            # Print results with confidence score
            print(f"--Tags in the local image {n}: ")
            if (len(tags_result_local.tags) == 0):
                print("----No tags detected.")
            else:
                for tag in tags_result_local.tags:
                    print("----'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))
            print()

'''

'''