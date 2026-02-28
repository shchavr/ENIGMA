import os

import faiss
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


class DocumentSearchService:
    def __init__(self, docs_path="app/docs"):
        self.docs_path = docs_path
        self.model = SentenceTransformer("intfloat/multilingual-e5-base")
        self.index = None
        self.text_chunks = []

        self._build_index()

    def _read_pdf(self, path):
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text

    def _chunk_text(self, text, chunk_size=500):
        chunks = []
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size].strip()
            if len(chunk) > 50:
                chunks.append(chunk)
        return chunks

    def _build_index(self):
        print("📚 Индексация PDF документации...")

        for file in os.listdir(self.docs_path):
            if file.endswith(".pdf"):
                path = os.path.join(self.docs_path, file)
                text = self._read_pdf(path)
                chunks = self._chunk_text(text)
                self.text_chunks.extend(chunks)

        if not self.text_chunks:
            print("⚠️ PDF файлы не найдены или пустые")
            return

        embeddings = self.model.encode(self.text_chunks, convert_to_numpy=True)

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

        print(f"✅ Индекс создан. Чанков: {len(self.text_chunks)}")

    def search(self, query, k=5):
        if not self.index or not query:
            return []

        query_embedding = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding, k)

        results = []
        for i in indices[0]:
            if i < len(self.text_chunks):
                results.append(self.text_chunks[i])

        return results
