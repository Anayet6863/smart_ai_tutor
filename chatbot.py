import os
from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnableParallel
from langchain_groq import ChatGroq

from prompts import (
    KEYWORDS_PROMPT,
    SUMMARY_PROMPT,
    STRUCTURED_OUTPUT_PROMPT,
)
from schemas import ChatbotResponse


def _route_question(data: dict[str, Any]) -> str:

    question = data["question"].lower()

    programming_terms = (
        "python", "javascript", "java", "programming", "code", "coding",
        "bug", "debug", "function", "class", "api", "html", "css", "sql",
        "algorithm", "data structure", "error", "exception",
    )
    math_terms = (
        "math", "mathematics", "calculate", "equation", "algebra", "geometry",
        "derivative", "integral", "probability", "statistics", "fraction",
        "percentage", "solve", "quadratic", "trigonometry",
    )

    if any(term in question for term in programming_terms):
        return "programming"
    if any(term in question for term in math_terms):
        return "mathematics"
    return "general"


def build_chatbot():

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "Something is wrong. "
        )

    model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    llm = ChatGroq(
        model=model_name,
        temperature=0.2,
        api_key=api_key,
    )
    text_parser = StrOutputParser()

    programming_prompt = PromptTemplate.from_template(
        "You are a patient programming tutor. Explain code accurately, "
        "use a small example when helpful, and avoid assuming prior knowledge.\n\n"
        "User question: {question}"
    )
    mathematics_prompt = PromptTemplate.from_template(
        "You are a patient mathematics tutor. Explain the reasoning step by "
        "step, show calculations where appropriate, and check the result.\n\n"
        "User question: {question}"
    )
    general_prompt = PromptTemplate.from_template(
        "You are a helpful general assistant. Give a clear, accurate answer "
        "at a beginner-friendly level. If a question is ambiguous, say so.\n\n"
        "User question: {question}"
    )

    route_branch = RunnableBranch(
        (
            lambda data: _route_question(data) == "programming",
            programming_prompt | llm | text_parser,
        ),
        (
            lambda data: _route_question(data) == "mathematics",
            mathematics_prompt | llm | text_parser,
        ),
        general_prompt | llm | text_parser,
    )

    summary_chain = SUMMARY_PROMPT | llm | text_parser
    keywords_chain = KEYWORDS_PROMPT | llm | text_parser

    parallel_chain = RunnableParallel(
        question=RunnableLambda(lambda data: data["question"]),
        answer=route_branch,
        summary=summary_chain,
        keywords=keywords_chain,
        category=RunnableLambda(lambda data: _route_question(data)),
    )

    structured_llm = llm.with_structured_output(ChatbotResponse)
    structured_chain = STRUCTURED_OUTPUT_PROMPT | structured_llm

    return parallel_chain | structured_chain
