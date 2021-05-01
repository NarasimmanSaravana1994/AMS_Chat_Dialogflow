from pydantic import BaseModel


class NLU_Request_Object(BaseModel):
    companyid = int
    domainid: int
    questionid: int
    answer: str
