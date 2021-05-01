import requests
''' application modules '''
from database_utils.mongo_utils import mongo_db_util
from models import responce_model as responce_model_object
from email_services import email

''' find the intent using web service approch '''


def find_nlu_intent(company_id: int, domain_id: int, question_id: int, answer: str) -> str:

    url = f"http://localhost:8002/nlu-services/"

    request = {"company_id": company_id, "domain_id": domain_id,
               "question_id": question_id, "answer": answer}
    response = requests.post(url, data=request)

    if response.status_code == 200:
        print(response.content.decode('utf-8'))
        return response.json
    else:
        return ""


''' verify the user answer '''


def verify_user_answer(company_id: int, domain_id: int, question_id: int, answer: str):
    base_flows = mongo_db_util.get_base_flow(
        company_id=company_id, domain_id=domain_id)

    for index, base_flow in enumerate(base_flows):
        if base_flow["question_id"] == question_id:

            if base_flow["is_nlu"]:
                return True, find_nlu_intent(company_id=company_id, domain_id=domain_id, question_id1=question_id, answer=answer)
            elif base_flow["is_db_provider"] and len(base_flow["answers"]):
                return True, base_flow["next_question_id"]
            else:
                for base_flow_answer in base_flow["answers"]:
                    if answer in base_flow_answer:
                        return True, base_flow_answer["mapped_question_id"]


''' identify the next flow based on user responce '''


def identify_next_dialogflow(company_id: int, domain_id: int, question_id: int) -> responce_model_object:

    base_flows = mongo_db_util.get_base_flow(
        company_id=company_id, domain_id=domain_id)

    chat_responce = []
    for base_flow in enumerate(base_flows):

        if base_flow['question_id'] == question_id:
            chat_responce = base_flow
            break
    return chat_responce


''' chat dialog flow '''


def chat_dialogflow(session_id: int, company_id: int, domain_id: int) -> responce_model_object:
    ''' get the user chat history based on user session id '''
    user_chat_dialog_history = mongo_db_util.get_chat_history_with_session_id(
        session_id=session_id)

    question_id = user_chat_dialog_history[-1]['question_id']
    answer = user_chat_dialog_history[-1]['answer']

    ''' verfiy the user answer'''
    is_user_answer_verified, next_question_id = verify_user_answer(
        company_id=company_id, domain_id=domain_id, question_id=question_id, answer=answer)

    ''' identify the next flow based on user responce '''
    if is_user_answer_verified:
        next_dialogflow = identify_next_dialogflow(
            company_id=company_id, domain_id=domain_id, question_id=next_question_id)
    else:
        next_dialogflow = identify_next_dialogflow(
            company_id=company_id, domain_id=domain_id, question_id=question_id)

    if next_dialogflow["flow_end"]:
        email.Email_triggering(session_id, company_id,
                               domain_id).email_sending()

    return next_dialogflow
