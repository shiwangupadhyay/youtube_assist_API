from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from langchain_community.document_loaders import YoutubeLoader
from dotenv import load_dotenv
from chat_models.models import Summarizer_model
from config.constants import VERSION
from schema.user_input import SummarizerInput
from prompts.prompt_templates import summarizer_template

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
        loader = YoutubeLoader.from_youtube_url(
            url,
            language=["en", "hi"]
        )
        docs = loader.load()

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



