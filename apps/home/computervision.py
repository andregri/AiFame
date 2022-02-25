from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes

from collections import defaultdict


async def detect_objects(computervision_client, image_url):
    """Detect objects from a remote image"""
    detect_objects_results_local = \
        computervision_client.detect_objects(image_url)

    return detect_objects_results_local.objects


async def tag_object(computervision_client, image_urls):
    """Tag remote image"""
    result = defaultdict(int)
    for url in image_urls:
        tags = computervision_client.tag_image(url)
        # Filter tags (remove food and fruit)
        result[tags[0]] += 1
    return tags
