from pydantic import BaseModel, EmailStr
from typing import List

class userCreate(BaseModel):
    email: str
    password: str
    role:str = "student"

class userOut(BaseModel):
    email: str
    role:str = "student"

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ExamCreate(BaseModel):
    title: str
    duration: int

class ExamCreateOut(BaseModel):
    id: int
    title: str
    duration: int

    class Config:
        orm_mode = True

class QuestionOut(BaseModel):
    id: int

    text: str

    option_a: str
    option_b: str
    option_c: str
    option_d: str

    class Config:
        orm_mode = True


class ExamOut(BaseModel):
    id: int
    title: str
    duration: int

    questions: List[QuestionOut]

    class Config:
        orm_mode = True

class AnswerInput(BaseModel):
    question_id: int
    answer: str


class SubmitExam(BaseModel):
    answers: List[AnswerInput]

class QuestionCreate(BaseModel):
    text: str

    option_a: str
    option_b: str
    option_c: str
    option_d: str

    correct_answer: str