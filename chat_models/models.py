from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv
from schema.output_schema import SummarizerOutput

load_dotenv()

llama = ChatNVIDIA(
  model="meta/llama-3.3-70b-instruct", 
  temperature=0.6,
  top_p=0.7,
  max_tokens=4096,
)
Summarizer_model = llama.with_structured_output(SummarizerOutput)

quiz_model = llama

chat_model = llama