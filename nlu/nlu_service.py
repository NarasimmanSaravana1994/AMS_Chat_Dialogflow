from fastapi import Request, FastAPI
import uvicorn

''' application modules '''
from models import nlu_request
from load_model import predict


app = FastAPI()


@app.post("/nlu-services",
          resquest_data=nlu_request.NLU_Request_Object,
          responses={
              200: {
                  "content": {"application/json": {"example": {"question__id": 1, "answer": "user example chat.."}},
                              "description": "Return the predicted intent",
                              }}}
          )
async def nlu_services(nlu_requests: nlu_request.NLU_Request_Object):

    ''' gathering required property for nlu service to predict the intent '''
    company_id = nlu_requests.companyid
    domain_id = nlu_requests.domainid
    question_id = nlu_requests.questionid
    answer = nlu_requests.answer

    return predict(company_id, domain_id, question_id, answer)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)