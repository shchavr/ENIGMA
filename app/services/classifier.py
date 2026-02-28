from transformers import pipeline
from app.config import CATEGORIES


class ClassificationService:
    def __init__(self):
        self.model = pipeline(
            "zero-shot-classification",
            model="joeddav/xlm-roberta-large-xnli"
        )

    def classify(self, text: str) -> dict:
        result = self.model(text, candidate_labels=CATEGORIES)

        return {
            "category": result["labels"][0],
            "confidence": round(float(result["scores"][0]), 4)
        }