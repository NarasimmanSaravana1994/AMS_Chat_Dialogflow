from fastapi import Request, FastAPI
import uvicorn

''' application modules '''
from model_files import request_model
from model_files import responce_model

app = FastAPI()


@app.post("/chat-services",
          resquest_data=request_model.Request_Object,
          response_model=responce_model.Responce_Object,
          responses={
              200: {
                  "content": {"application/json": {"example": {"question_id": 1, "question": "Hi this is AMS chatbot service"}},
                              "description": "Return the chat dialogflow mandatory properties.",
                              }}}
          )
async def chat_services():
    return {"msg": "success"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
