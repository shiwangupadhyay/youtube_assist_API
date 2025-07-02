from langchain_core.prompts import PromptTemplate


summarizer_template = PromptTemplate(
    template="""
You are a helpful assistant skilled at summarizing spoken content into clear, concise summaries.

Below is the transcript of a YouTube video. Summarize the main points, key ideas, and relevant details in a way that is informative and easy to understand.

Write the summary in professional yet engaging language. Keep it under 200 words.

Transcript:
---
{transcript}
---
""",
input_variables=['transcript']
)