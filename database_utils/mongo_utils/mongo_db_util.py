from pymongo import MongoClient
from bson.json_util import dumps
import json
from ConfigParser import SafeConfigParser

''' database configuration parser and connections '''
parser = SafeConfigParser()
parser.read('db.ini')

url = parser.get('mongo_database_congfiguration_details', 'url')
port = parser.get('mongo_database_congfiguration_details', 'port')

''' connecting the mongodb '''
client = MongoClient(url, port)

''' dialog flow collection '''
db_dialog_flow = client.amschatdialogflow

''' model collection '''
db_dialog_flow = client.nlu_models

session = db_dialog_flow.get_collection('session')
dialog_flow = db_dialog_flow.get_collection('dialog_flows')

exist_nlu_model = db_dialog_flow.get_collection("exists_nlu_models")

''' check the session id is exist or not '''
def is_sessionid_exists(session_id: int) -> bool:
    try:
        if session.find({"session_id": session_id}).count() == 1:
            return True
        else:
            return False
    except Exception as ex:
        return False

''' insert new session id '''
def insert_collection(session_id: int) -> bool:
    try:
        session.insert_one({"session_id": str(session_id),
                            "status": "True", "chat_dialogflow": []})
        return True
    except Exception as ex:
        return False

''' upate the user chat responce in mongo '''
def update_chat_dialogflow(session_id, chat_dialogflow) -> bool:
    try:
        '''
        is_exit = session.find({"$and": [{"session_id": session_id}, {
                               "chat_flow.question_id": chat_flow['question_id']}]}).count()

        if is_exit == 1:
            session.update({"$and": [{"session_id": session_id}, {"chat_flow.question_id": chat_flow['question_id']}]}, {
                           "$set": {"chat_flow.$.answer": chat_flow['answer']}})
        else:
        '''
        session.update_one(
            {
                "session_id": str(session_id)},
            {
                "$push": {
                    "chat_dialogflow": chat_dialogflow
                }
            }
        )

    except Exception as ex:
        return False

    return True

''' get the user chat history based on session id '''
def get_chat_history_with_session_id(session_id: int) -> {}:
    try:
        return json.loads(dumps(session.find_one({"session_id": session_id}, {"_id": 0})))["chat_dialogflow"]
    except Exception as ex:
        return {}

''' get dialogflow collection based on comapny id and  domain id '''
def get_base_flow(company_id: int, domain_id: int) -> {}:
    return json.loads(dumps(dialog_flow.find_one({"company_id": company_id, "domain_id": domain_id})))


''' get the model path nlu approach '''
def get_model_path(company_id: int, domain_id: int, question_id: int) -> str:
    return json.loads(dumps(dialog_flow.find_one({"company_id": company_id, "domain_id": domain_id}, {"questions": {"elemMatch": {"question_id": question_id}}})))

def load_model_run_time():
    return json.loads(dumps(exist_nlu_model.find_one({'is_loded':False})))