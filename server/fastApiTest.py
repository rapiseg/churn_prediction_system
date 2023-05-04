import json

import jwt
import pandas as pd
from fastapi import FastAPI, HTTPException, Response, Form, File, UploadFile, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import hashlib
import datetime
from passlib.hash import bcrypt
from typing import Union
from pydantic import BaseModel
import util

from typing_extensions import Annotated

app = FastAPI()

# CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


class Dataset(BaseModel):
    token: str
    filename: str
    contents: str


class SelectedDataset(BaseModel):
    token: str
    filename: str


class Token(BaseModel):
    token: str


# Connect to MongoDB
try:
    client = MongoClient(
        "mongodb+srv://admin:N8ugERgswgfnB8JP@mycluster.6ag11nz.mongodb.net/?retryWrites=true&w=majority")
    db = client["mydb"]
    dataset_collection = db["datasets"]
    users_collection = db["users"]
    print("Connected")
except:
    print("connection error")


try:
    util.load_models()
    print("Successfully loaded models")
except:
    print("Failed to load models")

# Define the User class
class User:
    def register(self, username, password):
        hashed_password = bcrypt.hash(password)
        users_collection.insert_one({"username": username, "password": hashed_password})

    def login(self, username, password):
        user = users_collection.find_one({"username": username})
        if user and bcrypt.verify(password, user["password"]):
            token = JWTAuthenticator.encode_token({"username": username})
            return token
        else:
            return None


# Define the JWTAuthenticator class
class JWTAuthenticator:
    @staticmethod
    def encode_token(claims):
        encoded = jwt.encode(claims, "jwt_secret", algorithm="HS256")
        return encoded

    @staticmethod
    def decode_token(token):
        try:
            decoded = jwt.decode(token, "jwt_secret", algorithms=["HS256"])
            return decoded
        except:
            return None


# JWT settings
app_secret_key = '38dd56f56d405e02ec0ba4be4607eaab'


@app.post("/api/v1/register")
async def register(userdata: dict):
    # Checking if user already exists in database
    existing_user = users_collection.find_one({"username": userdata["username"]})
    if existing_user:

        raise HTTPException(status_code=400, detail="Username already exists")

    user = User().register(userdata["username"], userdata["password"])

    token = jwt.encode({"username": userdata["username"]}, app_secret_key, algorithm='HS256')

    # Creating and returning response
    response = {
        "username": userdata["username"],
        "token": token,
        "message": "User registered successfully",
        "status_code": 200
    }
    return response


@app.post("/api/v1/login")
async def login(userdata: dict):
    # Checking if user exists in database or not
    token = User().login(userdata["username"], userdata["password"])
    if token:
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": userdata["username"],
            "status_code": 200
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

from requests_toolbelt.multipart.encoder import MultipartEncoder
import base64
@app.post("/api/v1/upload_file")
async def upload_file(request: Request):
    # Get the MultipartEncoder object from the request body
    form = await request.form()

    # Extract the file and session token from the MultipartEncoder object
    encoder = MultipartEncoder(form)
    token = encoder.fields["session_token"]

    if token:
        file = encoder.fields["file"]
        file_name = encoder.fields["filename"]
        file = file.encode('utf-8')
        encoded_string = base64.b64encode(file)

        datasetDoc = {
            "username": JWTAuthenticator.decode_token(token)["username"],
            "filename": file_name,
            "contents": encoded_string
        }
        dataset_collection.insert_one(datasetDoc)
        return {"status_code": 200,
                "message": "Dataset saved successfully"}
    else:
        raise HTTPException(status_code=401, detail="Please Login")



# @app.post("/api/v1/upload")
# async def upload_csv(dataset: Dataset):
#     token = dataset.token
#     if token:
#         username = JWTAuthenticator.decode_token(token)["username"]
#         datasetDoc = {
#             "username": username,
#             "filename": dataset.filename,
#             "contents": dataset.contents.encode("utf-8")
#         }
#         dataset_collection.insert_one(datasetDoc)
#         return {"status_code": 200,
#                 "message": "Dataset saved successfully"}
#     else:
#         raise HTTPException(status_code=401, detail="Please Login")

@app.get("/api/v1/filenames")
async def get_all_filenames(token: Token):
    token = token.token
    if token:
        username = JWTAuthenticator.decode_token(token)["username"]
        datasets = dataset_collection.find({"username": username})
        filenames = [file["filename"] for file in datasets]
        if filenames:
            return {"filenames": filenames, "status_code": 200}
        else:
            return {"filenames": "No files", "status_code": 400}
    else:
        raise HTTPException(status_code=401, detail="Please Login")


@app.get("/api/v1/dataset")
async def get_dataset(userdata: dict):
    token = userdata["token"]
    filename = userdata["filename"]
    if token:
        username = JWTAuthenticator.decode_token(token)["username"]
        doc = dataset_collection.find_one({"username": username, "filename": filename})
        if doc:
            decoded_dataset = base64.b64decode(doc['contents'])
            return ({"status_code":200, "dataset":decoded_dataset})
        else:
            return ({"status_code": 400,
                 "message": f'File {filename} not found'
                 })
    else:
        raise HTTPException(status_code=401, detail="Please Login")


@app.delete("/api/v1/delete")
async def delete_dataset(selectedDataset: SelectedDataset):
    token = selectedDataset.token
    filename = selectedDataset.filename
    if token:
        username = JWTAuthenticator.decode_token(token)["username"]
        if dataset_collection.find_one({"username": username, "filename": filename}):
            dataset_collection.delete_one({"username": username, "filename": filename})
            return (
                {"status_code": 200,
                 "message": "Successfully deleted the dataset"
                 }
            )
        else:
            return (
                {"status_code": 400,
                 "message": f'File {filename} not found'
                 }
            )
    else:
        raise HTTPException(status_code=401, detail="Please Login")


@app.post("/predict_churn")
async def predict_churn(dataDict: dict):
    # print(type(dataDict))
    try:
        token = dataDict["token"]
        if token:
            if dataDict["inputType"] == 'single':
                df = pd.DataFrame(dataDict["featureDict"], index=[0])
            else:
                df = pd.DataFrame(dataDict["featureDict"])
            print(df.head())
            response = jsonable_encoder((util.get_predictions(df)).to_dict())
            return {"response": response, "status_code": 200}
        else:
            raise HTTPException(status_code=401, detail="Please Login")
    except Exception as e:
        print("Error:", str(e))

@app.get("/")
async def hello_world():
    return {"message": "Hello, World!"}


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
