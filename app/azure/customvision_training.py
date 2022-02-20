from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid, json


#Startup guide https://docs.microsoft.com/it-it/azure/cognitive-services/custom-vision-service/quickstarts/image-classification?tabs=visual-studio&pivots=programming-language-python

#Auth client
cred = json.load(open('.\\app\\azure\credentials.json'))
API_KEY_TRAIN = cred['API_KEY_CV_TRAIN']
ENDPOINT_TRAIN = cred['ENDPOINT_CV_TRAIN']
API_KEY_PRED = cred['API_KEY_CV_PRED']
ENDPOINT_PRED = cred['ENDPOINT_CV_PRED'] 


credentials = ApiKeyCredentials(in_headers={"Training-key": API_KEY_TRAIN})
trainer = CustomVisionTrainingClient(ENDPOINT_TRAIN, credentials)
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": API_KEY_PRED})
predictor = CustomVisionPredictionClient(ENDPOINT_TRAIN, prediction_credentials)

publish_iteration_name = "classifyModel"

credentials = ApiKeyCredentials(in_headers={"Training-key": API_KEY_TRAIN})
trainer = CustomVisionTrainingClient(ENDPOINT_TRAIN, credentials)

# Create a new project
print ("Creating project...")
project_name = uuid.uuid4()
project = trainer.create_project(project_name)

# Make two tags in the new project
hemlock_tag = trainer.create_tag(project.id, "Hemlock")
cherry_tag = trainer.create_tag(project.id, "Japanese Cherry")



# Load training set images
base_image_location = os.path.join (os.path.dirname(__file__), "Images")

print("Adding images...")

image_list = []

for image_num in range(1, 11):
    file_name = "hemlock_{}.jpg".format(image_num)
    with open(os.path.join (base_image_location, "Hemlock", file_name), "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[hemlock_tag.id]))

for image_num in range(1, 11):
    file_name = "japanese_cherry_{}.jpg".format(image_num)
    with open(os.path.join (base_image_location, "Japanese_Cherry", file_name), "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[cherry_tag.id]))

upload_result = trainer.create_images_from_files(project.id, ImageFileCreateBatch(images=image_list))
if not upload_result.is_batch_successful:
    print("Image batch upload failed.")
    for image in upload_result.images:
        print("Image status: ", image.status)
    exit(-1)



# Training the model
print ("Training...")
iteration = trainer.train_project(project.id)
while (iteration.status != "Completed"):
    iteration = trainer.get_iteration(project.id, iteration.id)
    print ("Training status: " + iteration.status)
    print ("Waiting 10 seconds...")
    time.sleep(10)



# The iteration is now trained. Publish it to the project endpoint
trainer.publish_iteration(project.id, iteration.id, publish_iteration_name, ENDPOINT_PRED)
print ("Done!")