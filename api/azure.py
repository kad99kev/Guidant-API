import requests
import os
import base64

from dotenv import load_dotenv
from pathlib import Path  # Python 3.6+ only


# from azure.cognitiveservices.vision.computervision import ComputerVisionClient
# from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
# from msrest.authentication import CognitiveServicesCredentials

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

_region = os.getenv("ACCOUNT_REGION")
_key = os.getenv("ACCOUNT_KEY")

# _credentials = CognitiveServicesCredentials(_key)
# _client = ComputerVisionClient(
#     endpoint="https://" + _region + ".api.cognitive.microsoft.com/",
#     credentials=_credentials,
# )


def describe_image(binary_image):
    url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/landmark.jpg"
    params = {"maxCandidates": "1", "language": "en"}
    headers = {
        # "Content-Type": "application/json",
        # "Content-Type": "multipart/form-data",
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": _key,
    }
    response = requests.post(
        "https://" + _region + ".api.cognitive.microsoft.com/vision/v3.1/describe",
        # json={"url": url},
        data=binary_image,
        params=params,
        headers=headers,
    )
    responseData = response.json()
    print(responseData)
    return responseData
