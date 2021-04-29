from pymongo import MongoClient
from bson.json_util import dumps
import json
from ConfigParser import SafeConfigParser

''' database configuration parser and connections '''
parser = SafeConfigParser()
parser.read('db.ini')

url = parser.get('mongo_database_congfiguration_details', 'url')
port = parser.get('mongo_database_congfiguration_details', 'port')

client = MongoClient(url, port)
db = client.amschatdialogflow
session = db.get_collection('session')
dialog_flow = db.get_collection('dialog_flow')


def is_sessionid_exists(session_id: int) -> bool:
    try:
        if session.find({"session_id": session_id}).count() == 1:
            return True
        else:
            return False
    except Exception as ex:
        return False


def insert_collection(session_id: int) -> bool:
    try:
        session.insert_one({"session_id": str(session_id),
                            "status": "True", "chat_flow": []})
        return True
    except Exception as ex:
        return False


def update_chat_dialogflow(session_id, chat_dialogflow):
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
