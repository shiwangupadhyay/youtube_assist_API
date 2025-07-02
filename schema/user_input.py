from pydantic import BaseModel, HttpUrl

class SummarizerInput(BaseModel):
    url : HttpUrl