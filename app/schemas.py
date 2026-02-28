from pydantic import BaseModel


class EmailRequest(BaseModel):
    text: str


class AnalysisResponse(BaseModel):
    sentiment: dict
    classification: dict
    extracted_data: dict
    generated_response: str