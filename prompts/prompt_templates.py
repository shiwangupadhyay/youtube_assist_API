from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from schema.output_schema import QuizOutput

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


parser = PydanticOutputParser(pydantic_object=QuizOutput)

quiz_template = PromptTemplate(
    template="""You are a quiz generator AI. Based on the following content, generate multiple-choice questions of varying difficulty.
    \n
    Content:
    \n
    {transcript}
    \n
    Instructions:
    - Generate a total of {number_of_questions} multiple-choice questions.
    - Divide them by difficulty: <EASY_COUNT> easy, <MEDIUM_COUNT> medium, <HARD_COUNT> hard.
    - Each question must include:
    - A clear and concise question
    - Four answer choices labeled A, B, C, and D
    - Indicate the correct answer (e.g., "Correct Answer: B")
    - Avoid vague or overly broad questions.
    - Focus on factual, conceptual, or inferential details mentioned in the content.
    - Ensure that hard questions require deeper understanding or inference.
    - Avoid repeating facts or overlapping questions.

    \n {format_instruction}
    """,
    input_variables=['transcript','number_of_questions'],
    partial_variables={'format_instruction':parser.get_format_instructions()}
    )