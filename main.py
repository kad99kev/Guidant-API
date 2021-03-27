from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from api import azure
from pydantic import BaseModel


class Item(BaseModel):
    name: str


app = FastAPI(debug=True)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def read_imagefile(file):
    print(BytesIO(file))
    image = BytesIO(file)
    return image


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/describe")
async def describe(image: UploadFile = File(...)):
    temp_file = image.file
    return azure.describe_image(temp_file.read())


@app.post("/read")
async def read(image: UploadFile = File(...)):
    temp_file = image.file
    return azure.read_image(temp_file.read())