import io
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from PIL import Image
from collections import defaultdict


async def detect_objects(computervision_client, image_url):
    """Detect objects from a remote image"""
    detect_objects_results_local = \
        computervision_client.detect_objects(image_url)

    return detect_objects_results_local.objects


async def tag_object(computervision_client, img_data):
    """Tag image"""
    tags = computervision_client.tag_image_in_stream(img_data)
    # Filter tags (remove food and fruit)
    index = 0
    for tag in tags.tags:
        if not 'food' in tag.name and not 'fruit' in tag.name: 
            return tags.tags[index].name
        index += 1
    return tags.tags[-1].name


def crop_image(img_data, box):
    img = Image.open(io.BytesIO(img_data))
    return img.crop(box)
