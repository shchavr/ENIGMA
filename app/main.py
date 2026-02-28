from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import EmailRequest
from app.services.classifier import ClassificationService
from app.services.document_search import DocumentSearchService
from app.services.extractor import ExtractionService
from app.services.response_gen import ResponseGenerator
from app.services.sentiment import SentimentService

app = FastAPI(title="AI Support ML Service", version="2.0")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sentiment_service = SentimentService()
classification_service = ClassificationService()
extraction_service = ExtractionService()
response_generator = ResponseGenerator()
document_service = DocumentSearchService()


@app.post("/ml/analyze")
def analyze_email(request: EmailRequest):
    text = request.text

    sentiment = sentiment_service.analyze(text)
    sentiment_label = sentiment["label"]

    classification = classification_service.classify(text)
    category = classification["category"]

    extracted = extraction_service.extract_all(text, sentiment_label)
    extracted["category"] = category

    search_query = f"{extracted.get('device_type', '')} {extracted.get('summary', '')}"
    docs_context = document_service.search(search_query)

    generated_response = response_generator.generate(
        extracted,
        category,
        docs_context
    )

    return {
        "sentiment": sentiment,
        "classification": classification,
        "extracted_data": extracted,
        "documentation_context": docs_context,
        "generated_response": generated_response
    }
