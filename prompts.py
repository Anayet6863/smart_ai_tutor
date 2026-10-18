from langchain_core.prompts import PromptTemplate

SUMMARY_PROMPT = PromptTemplate.from_template(
    "Summarize the key point of the user's question in 1-3 short sentences."
    "Do not answer at length, summarize the likely topic and intent.\n\n"
    "Question: {question}"
)

KEYWORDS_PROMPT = PromptTemplate.from_template(
    "Return 3 to 6 concise keywords or short phrases that represent the "
    "user's question. Return only a comma-separated list, without a heading.\n\n"
    "Question: {question}"
)

STRUCTURED_OUTPUT_PROMPT = PromptTemplate.from_template(
    """You are formatting an AI tutor response into a structured result.
Use the supplied generated content as the starting point. Keep the answer
helpful and coherent. The category must be one of: programming, mathematics,
general. The confidence field is a rough self-assessed estimate from 0.0 to
1.0, not a calibrated probability. Do not claim certainty when the question
is ambiguous or requires current information.

User question:
{question}

Routed answer:
{answer}

Summary:
{summary}

Keywords:
{keywords}

Detected category:
{category}
"""
)
