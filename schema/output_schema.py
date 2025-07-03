from pydantic import BaseModel, Field

class SummarizerOutput(BaseModel):
    title : str = Field(description='Title of the Video')
    summary : str = Field(description='Summary of the Video')

class QuizOutput(BaseModel):
    difficulty : str = Field(description='Difficulty of the Question')
    question : str = Field(description='Question in detail')
    option1 : str = Field(description='First Option for give question')
    option2 : str = Field(description='Second Option for give question')
    option3 : str = Field(description='Third Option for give question')
    option4 : str = Field(description='Fourth Option for give question')
    answer : str = Field(description='correct answer for the question')
