from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from doc_loader.transcript_loader import transcript_loader
from dotenv import load_dotenv
import json
import re
from chat_models.models import Summarizer_model, quiz_model
from config.constants import VERSION
from schema.user_input import SummarizerInput, QuizInput
from prompts.prompt_templates import summarizer_template, quiz_template

load_dotenv()

app = FastAPI()

@app.get('/')
def home():
    return{'message' : 'Youtube Assistant API'}

@app.get('/health')
def health_check():
    return {
        'status' : 'OK',
        'version' : VERSION
    }


@app.post("/summarizer")
async def transcript_summarizer(input_data: SummarizerInput):
    try:
        url = str(input_data.url)
        docs = transcript_loader(url)

        if not docs or not docs[0].page_content.strip():
            raise HTTPException(status_code=400, detail='Transcript is empty or could not be loaded.')

        transcript = docs[0].page_content

        chain = summarizer_template | Summarizer_model
        response = chain.invoke({'transcript': transcript})
        title = response.title
        summary = response.summary

        return JSONResponse(status_code=201, content={'message': {'title' : title,'summary' : summary}})

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Internal server error: {str(e)}')


@app.post("/quiz")
async def quiz_generator(input_data: QuizInput):
    try:
        url = str(input_data.url)
        docs = transcript_loader(url)

        if not docs or not docs[0].page_content.strip():
            raise HTTPException(status_code=400, detail='Transcript is empty or could not be loaded.')

        transcript = docs[0].page_content

        chain = quiz_template | quiz_model
        response = chain.invoke({'transcript': transcript,'number_of_questions' : input_data.no_of_questions})
        response = response.content

        match = re.search(r'```(?:json)?\s*(\[.*?\])\s*```', response, re.DOTALL)
        if not match:
            raise HTTPException(status_code=500, detail="Could not extract valid JSON from model response.")

        questions_json = match.group(1)

        # Step 3: Parse the JSON string to a Python list
        try:
            questions_data = json.loads(questions_json)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=500, detail=f"Invalid JSON format: {e}")

        # Step 4: Return the parsed JSON
        return JSONResponse(status_code=201, content={"questions": questions_data})

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Internal server error: {str(e)}')
