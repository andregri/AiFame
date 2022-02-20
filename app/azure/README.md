# detect_object_local.py

## Resources
https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts-sdk/image-analysis-client-library?tabs=visual-studio&pivots=programming-language-python

https://github.com/Azure-Samples/cognitive-services-quickstart-code/blob/master/python/ComputerVision/ImageAnalysisQuickstart.py

## Results
- Original image:
![original image](https://i.postimg.cc/FzgjnPmX/foods.jpg)

- Detected foods from original image:

| n | Tag | Confidence % | Bounding Box |
| - | --- | ------------ | ------------ |
| 0 | Fruit  | 0.556 | 316, 383, 92, 158  |
| 1 | :heavy_check_mark: orange | 0.584 | 416, 499, 127, 216 |
| 2 | :heavy_check_mark: orange | 0.524 | 331, 421, 165, 250 |
| 3 | Fruit  | 0.558 | 523, 596, 149, 213 |
| 4 | Food   | 0.537 | 577, 654, 189, 246 |
| 5 | Food   | 0.549 | 403, 483, 298, 376 |
| 6 | Food   | 0.621 | 593, 673, 443, 486 |
| 7 | Fruit  | 0.564 | 134, 236, 170, 278 |

- Analysis of each detected food

| n | Img | Description (confidence %) | Tags (% confidence) |
| - | --- | -------------------------- | ------------------- |
| 0 | ![](https://i.postimg.cc/8zybSnv1/0.jpg) | a close up of a bird  45.31% | `fruit` 97.53%, `apple` 96.30%, `natural foods` 90.97%, `food` 90.78%, `mcintosh` 90.20%, `produce` 86.68%, `red` 78.48%, `outdoor` 61.01% |
| 3 | ![](https://i.postimg.cc/bvs9NH01/3.jpg) | a green and yellow object 21.77% | `avocado` 99.29%, `fruit` 98.67%, `food` 86.35% |
| 4 | ![](https://i.postimg.cc/zf6SLbp6/4.jpg) | a round brown object on a green surface 46.02% | `avocado` 99.53%, `fruit` 97.88%, `food` 74.99% |
| 5 | ![](https://i.postimg.cc/j5f6yxF5/5.jpg) | a bowl of berries 37.08% | `fruit` with confidence 90.79%, `food` 87.99%, `superfood` 85.77%, `bowl` 74.66%, `berry` 68.51%, `peppercorn` 56.33% |
| 6 | ![](https://i.postimg.cc/L5MtTccV/6.jpg) | :x: too small | |

## Procedure
- Setup a python virtual environment
```bash
python3 -m venv azurevenv
source azurevenv/bin/activate
python3 -m pip install --upgrade pip
pip install --upgrade azure-cognitiveservices-vision-computervision
python3 -m pip install --upgrade Pillow
```

- Download the test image in `images/foods.jpg`
```
mkdir images && cd images
wget "https://www.grandecig.com/hs-fs/hubfs/images/blog_images/2020_Blog_Images/CompareTopDietTrends.jpg?width=730&name=CompareTopDietTrends.jpg" -o "foods.jpg"
```

- Write your credentials in `credentials.json`
```
{
    "API_KEY_CV_TRAIN":"past-here",
    "ENDPOINT_CV_TRAIN":"past-here",
    "API_KEY_CV_PRED":"past-here",
    "ENDPOINT_CV_PRED":"past-here",
    "API_KEY":"past-here",
    "ENDPOINT":"past_here"
}

```

- Run the script `python detect_object_local.py`
```
Detecting objects in local image:

Fruit with confidence 0.556 at location 316, 383, 92, 158
--Description of local image: 
----'a close up of a bird' with confidence 45.31%

--Tags in the local image 0: 
----'fruit' with confidence 97.53%
----'apple' with confidence 96.30%
----'natural foods' with confidence 90.97%
----'food' with confidence 90.78%
----'mcintosh' with confidence 90.20%
----'produce' with confidence 86.68%
----'red' with confidence 78.48%
----'outdoor' with confidence 61.01%

orange with confidence 0.584 at location 416, 499, 127, 216

orange with confidence 0.524 at location 331, 421, 165, 250

Fruit with confidence 0.558 at location 523, 596, 149, 213
--Description of local image: 
----'a green and yellow object' with confidence 21.77%

--Tags in the local image 3: 
----'avocado' with confidence 99.29%
----'fruit' with confidence 98.67%
----'food' with confidence 86.35%

Food with confidence 0.537 at location 577, 654, 189, 246
--Description of local image: 
----'a round brown object on a green surface' with confidence 46.02%

--Tags in the local image 4: 
----'avocado' with confidence 99.53%
----'fruit' with confidence 97.88%
----'food' with confidence 74.99%

Food with confidence 0.549 at location 403, 483, 298, 376
--Description of local image: 
----'a bowl of berries' with confidence 37.08%

--Tags in the local image 5: 
----'fruit' with confidence 90.79%
----'food' with confidence 87.99%
----'superfood' with confidence 85.77%
----'bowl' with confidence 74.66%
----'berry' with confidence 68.51%
----'peppercorn' with confidence 56.33%

Food with confidence 0.621 at location 593, 673, 443, 486
Traceback (most recent call last):
  File "detect_object_local.py", line 66, in <module>
    description_result = computervision_client.describe_image_in_stream(cropped_image)
  File "/home/andrea/Documents/progetto_python/AiFame/app/azure/azurevenv/lib/python3.7/site-packages/azure/cognitiveservices/vision/computervision/operations/_computer_vision_client_operations.py", line 1191, in describe_image_in_stream
    raise models.ComputerVisionErrorResponseException(self._deserialize, response)
azure.cognitiveservices.vision.computervision.models._models_py3.ComputerVisionErrorResponseException: (InvalidRequest) Image must be at least 50 pixels in width and height
```