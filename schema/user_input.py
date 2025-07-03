from pydantic import BaseModel, HttpUrl, Field

class SummarizerInput(BaseModel):
    url : HttpUrl = Field(...,description='URL of the Youtube Video to Summarize.')

class QuizInput(BaseModel):
    url : HttpUrl = Field(...,description='URL of the Youtube Video to generate Quiz.')
    no_of_questions : int = Field(...,description='No. of Questions You want to generate.')

class ChatInput(BaseModel):
    url : HttpUrl = Field(...,description='URL of the Youtube Video to chat from.')
    query : str = Field(...,description='Enter your Query you want answer of.')
    session_id: str = Field(..., description='Unique session ID.')