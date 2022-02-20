
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid, json

from azureml.core.model import Model


model = Model(ws, 'classifyModel')


#Auth client
cred = json.load(open('.\\app\\azure\credentials.json'))
API_KEY_PRED = cred['API_KEY_CV_PRED']
ENDPOINT_PRED = cred['ENDPOINT_CV_PRED'] 

# Now there is a trained endpoint that can be used to make a prediction
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": API_KEY_PRED})
predictor = CustomVisionPredictionClient(ENDPOINT_PRED, prediction_credentials)


with open(os.path.join ("Test/test_image.jpg"), "rb") as image_contents:
    results = predictor.classify_image(
        project.id, publish_iteration_name, image_contents.read())

    # Display the results.
    for prediction in results.predictions:
        print("\t" + prediction.tag_name +
              ": {0:.2f}%".format(prediction.probability * 100))