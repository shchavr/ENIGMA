from transformers import pipeline


class SentimentService:
    def __init__(self):
        self.model = pipeline(
            "sentiment-analysis",
            model="blanchefort/rubert-base-cased-sentiment"
        )

    def analyze(self, text: str) -> dict:
        result = self.model(text)[0]
        return {
            "label": result["label"],
            "confidence": round(float(result["score"]), 4)
        }