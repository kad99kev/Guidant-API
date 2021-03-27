import requests
import os
import base64

from dotenv import load_dotenv
from pathlib import Path


_env_path = Path(".") / ".env"
load_dotenv(dotenv_path=_env_path)

_region = os.getenv("ACCOUNT_REGION")
_key = os.getenv("ACCOUNT_KEY")


def describe_image(binary_image):
    params = {"maxCandidates": "1", "language": "en"}
    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": _key,
    }
    response = requests.post(
        "https://" + _region + ".api.cognitive.microsoft.com/vision/v3.1/describe",
        data=binary_image,
        params=params,
        headers=headers,
    )
    response_data = response.json()
    print(response_data)
    return response_data


def read_image(binary_image):
    params = {"language": "en"}
    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": _key,
    }
    response = requests.post(
        "https://" + _region + ".api.cognitive.microsoft.com/vision/v3.1/read/analyze",
        data=binary_image,
        params=params,
        headers=headers,
    )
    received_result = False
    while not received_result:
        read_url = response.headers["Operation-Location"]
        read_response = requests.get(
            read_url,
            headers={"Ocp-Apim-Subscription-Key": _key},
        )
        read_response = read_response.json()
        if read_response["status"] == "succeeded":
            received_result = True
    texts = []
    for line in read_response["analyzeResult"]["readResults"][0]["lines"]:
        texts.append(line["text"])
    return {"texts": texts}