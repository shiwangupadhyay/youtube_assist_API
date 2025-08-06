from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from schema.output_schema import SummarizerOutput

load_dotenv()

llama = ChatNVIDIA(
  model="meta/llama-3.3-70b-instruct", 
  temperature=0.6,
  top_p=0.7,
  max_tokens=4096,
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.5,
    max_tokens=None
)
Summarizer_model = llm.with_structured_output(SummarizerOutput)

quiz_model = llm

chat_model = llm