import requests
import os
import base64
import re

from dotenv import load_dotenv
from pathlib import Path
from pydub import AudioSegment

_env_path = Path(".") / ".env"
load_dotenv(dotenv_path=_env_path)

_region = os.getenv("ACCOUNT_REGION")
_vision_key = os.getenv("VISION_KEY")
_voice_key = os.getenv("VOICE_KEY")


def describe_image(binary_image):
    params = {"maxCandidates": "1", "language": "en"}
    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": _vision_key,
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
        "Ocp-Apim-Subscription-Key": _vision_key,
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
            headers={"Ocp-Apim-Subscription-Key": _vision_key},
        )
        read_response = read_response.json()
        if read_response["status"] == "succeeded":
            received_result = True
    texts = []
    for line in read_response["analyzeResult"]["readResults"][0]["lines"]:
        texts.append(line["text"])
    print(texts)
    return {"texts": texts}


def convert_to_wav(audio_file):
    sound = AudioSegment.from_file(audio_file, "m4a")
    sound.export(audio_file, format="wav")


def get_command(audio_file, ends_with_m4a):
    if ends_with_m4a:
        convert_to_wav(audio_file)
    params = {"language": "en-IN"}
    headers = {
        "Content-Type": "audio/wav",
        "Ocp-Apim-Subscription-Key": _voice_key,
    }
    response = requests.post(
        "https://"
        + _region
        + ".stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1",
        data=audio_file,
        params=params,
        headers=headers,
    )
    try:
        voice_data = response.json()
        print(re.sub(r"[^\w\s]", "", voice_data["DisplayText"]).lower())
        return {"command": re.sub(r"[^\w\s]", "", voice_data["DisplayText"]).lower()}
    except:
        print(response.status_code, response.reason)
        return {response.status_code: response.reason}