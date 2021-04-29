from pydantic import BaseModel


class Request_Object(BaseModel):
    sessionid: str
    companyid = int
    domainid: int
    questionid: int
