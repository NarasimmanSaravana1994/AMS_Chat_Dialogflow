from fastapi import Request, FastAPI,File, Form, UploadFile
import uvicorn

''' application modules '''
from model_files import request_model
from model_files import responce_model
from database_utils.mongo_utils import mongo_db_util
from database_utils.sql_utils import sql_db_util

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
async def chat_services(chat_request: request_model.Request_Object):
    
    ''' getting the mandatory properties for chat dialogflow'''
    session_id = chat_request.sessionid
    company_id = chat_request.companyid
    domain_id = chat_request.domainid
    question_id = chat_request.questionid
    user_chat = chat_request.userchat

    new_session = False

    ''' check session is exist or not, if not exit create a new session with the help of client browser session id'''
    if not await mongo_db_util.is_sessionid_exists(session_id=session_id):
        await mongo_db_util.insert_collection(session_id=session_id)
        question_id = 1
        new_session = True
    
    if not new_session:
        await mongo_db_util.update_chat_dialogflow(session_id=session_id, chat_dialogflow=chat_request)
    
    ## flow part need to implement ###
    return {"msg": "success"}

@app.post("/upload-file/")
async def upload_file(uploded_file: UploadFile = File(...)):
    os.mkdir("files")
    file_name = os.getcwd()+"/files/"+uploded_file.filename.replace(" ", "-")
    with open(file_name,'wb+') as f:
        f.write(uploded_file.file.read())
        f.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
