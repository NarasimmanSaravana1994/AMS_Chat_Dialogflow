import os
import requests
import uvicorn
from fastapi import Body, FastAPI, status, Request
from typing import Optional, Set
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, UJSONResponse
from fastapi.middleware.cors import CORSMiddleware

tags_metadata = [
    {
        "name": "Chatbot testing gateway services",
        "description": "This is a service for chat request and chat dialog flow creation services",
        "externalDocs": {"description": "Items external docs",
                         "url": "https://fastapi.tiangolo.com/", }
    }
]

app = FastAPI(
    # servers=[
    # {"url": "https://localhost", "description": "Staging environment"},
    # {"url": "https://localhost", "description": "Production environment"},],
    openapi_tags=tags_metadata,
    docs_url="/api_documentation", redoc_url=None)

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/", response_class=UJSONResponse, include_in_schema=True, tags=["Chatbot testing gateway services"])
async def test(request: Request):

    responce = {"applicetion_code": "0001",
                "message": "gatway service is working fine", "clients_ip": request.client.host}
    headers = {"Content-Language": "en-US",
               "Cache-Control": "no-cache,no-store,max-age=0,private"}
    json_compatible_responce = jsonable_encoder(responce)

    return JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_responce, headers=headers, media_type="application/json")


async def test_function():

    request_example = {"test": "in"}

    get_test_url = f"http://localhost:8001/test/"

    test_get_response = requests.post(get_test_url, data=request_example)

    if test_get_response .status_code == 200:
        print(test_get_response.content.decode('utf-8'))
        return True


@app.post("/chat-service", response_class=UJSONResponse, include_in_schema=True, tags=["chat dialogflow services"])
async def chat_services(request: Request):

    responce = {"applicetion_code": "0002",
                "message": "chat dialogflow service is working fine"}
    headers = {"Content-Language": "en-US",
               "Cache-Control": "no-cache,no-store,max-age=0,private"}
    json_compatible_responce = jsonable_encoder(responce)

    await test_function()

    return JSONResponse(status_code=status.HTTP_200_OK, content=json_compatible_responce, headers=headers, media_type="application/json")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
