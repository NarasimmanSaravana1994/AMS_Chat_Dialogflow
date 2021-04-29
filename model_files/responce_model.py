from pydantic import BaseModel
from enum import Enum


class Input_Type(Enum):
    datatime
    string
    integer
    flietype
    custome_int


class Responce_Object(BaseModel):
    question_id: int
    question = str
    input_type: Input_Type
    flow_end: bool
    option_answers: list
    error_msg: str
