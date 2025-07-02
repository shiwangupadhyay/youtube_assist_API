from pydantic import BaseModel, Field

class SummarizerOutput(BaseModel):
    title : str = Field(description='Title of the Video')
    summary : str = Field(description='Summary of the Video')