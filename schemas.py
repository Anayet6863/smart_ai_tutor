from typing import Literal
from pydantic import BaseModel, Field, field_validator


class ChatbotResponse(BaseModel):

    answer: str = Field(description="A clear and helpful answer to the user.")
    summary: str = Field(description="A concise summary of the response.")
    confidence: float = Field(
        ge=0.0,
        le=1.0,
    
    )
    category: Literal["programming", "mathematics", "general"] = Field(
    )
    keywords: list[str] = Field(
        min_length=1,

    )

    @field_validator("keywords")
    @classmethod
    def remove_empty_keywords(cls, values: list[str]) -> list[str]:
        cleaned = [value.strip() for value in values if value.strip()]
        if not cleaned:
            raise ValueError("At least one non-empty keyword is required.")
        return cleaned
