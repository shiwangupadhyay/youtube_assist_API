import json
import re
from langchain.schema import AIMessage, HumanMessage
from langchain.memory import ConversationBufferMemory
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from doc_loader.transcript_loader import transcript_loader
from dotenv import load_dotenv
from chat_models.models import Summarizer_model, quiz_model, chat_model
from config.constants import VERSION, MAX_HISTORY
from schema.user_input import SummarizerInput, QuizInput, ChatInput
from prompts.prompt_templates import summarizer_template, quiz_template

load_dotenv()

app = FastAPI()

session_store = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace '*' with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    


def get_session_memory(session_id: str):
    if session_id not in session_store:
        session_store[session_id] = {"history": []}
    return session_store[session_id]

    
from schema.user_input import ChatInput

@app.post("/chat")
async def chat(input_data: ChatInput):
    try:
        url = str(input_data.url)
        transcript_doc = transcript_loader(url)
        if not transcript_doc or not transcript_doc[0].page_content.strip():
            raise HTTPException(status_code=400, detail='Transcript is empty or could not be loaded.')

        transcript = transcript_doc[0].page_content
        session = get_session_memory(input_data.session_id)

        session["history"].append(HumanMessage(content=input_data.query))

        if len(session["history"]) > MAX_HISTORY * 2:
            session["history"] = session["history"][-MAX_HISTORY*2:]

        context = f"Transcript:\n{transcript}\n\nConversation:\n" + "\n".join([
            f"Human: {msg.content}" if isinstance(msg, HumanMessage) else f"AI: {msg.content}"
            for msg in session["history"]
        ])

        response = chat_model([HumanMessage(content=context)])

        session["history"].append(AIMessage(content=response.content))

        return JSONResponse(status_code=200, content={"response": response.content})

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Internal server error: {str(e)}')

@app.post("/chat/reset")
async def reset_chat(session_id: str = Query(..., description="Session ID to reset")):
    if session_id in session_store:
        del session_store[session_id]
    return {"message": "Session reset successfully."}
