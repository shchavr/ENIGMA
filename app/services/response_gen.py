import os
from groq import Groq


FIELD_NAMES_RU = {
    "full_name": "ФИО",
    "object": "Объект",
    "date": "Дата",
    "phone": "Телефон",
    "factory_number": "Заводской номер"
}


class ResponseGenerator:
    def __init__(self):
        try:
            self.client = Groq(
                        api_key="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"
                    )
            self.model = "llama-3.3-70b-versatile"
            self.use_groq = True
            print("✅ ResponseGenerator: Groq подключен")
        except:
            self.use_groq = False
            print("⚠️ ResponseGenerator: Groq недоступен")

    def generate(self, extracted_data: dict, category: str, docs_context: list = None):

        device_type = extracted_data.get("device_type")

        # 🚨 Без устройства RAG невозможен
        if not device_type:
            return self._request_device_type(extracted_data)

        # Генерация с документацией
        if self.use_groq:
            return self._groq_response(extracted_data, category, docs_context)

        return self._template_fallback(extracted_data)

    # ---------------------------------------------------------
    # 🔥 Основная продакшен-логика
    # ---------------------------------------------------------

    def _groq_response(self, extracted_data, category, docs_context):

        cleaned_docs = self._clean_documentation(docs_context)

        missing_optional = [
            FIELD_NAMES_RU.get(f)
            for f in ["factory_number", "object", "phone"]
            if not extracted_data.get(f)
        ]

        context = f"""
Категория: {category}
Устройство: {extracted_data.get('device_type')}
Проблема: {extracted_data.get('summary')}
Эмоция клиента: {extracted_data.get('emotion')}
"""

        prompt = f"""
Ты инженер технической поддержки.

Ниже фрагменты официальной документации:
{cleaned_docs}

Информация о запросе клиента:
{context}

Сформируй связный профессиональный ответ:

1. Кратко подтвердить понимание проблемы
2. Дать конкретные рекомендации на основе документации
3. НЕ цитировать документацию дословно
4. НЕ вставлять мусор (рисунки, номера страниц, ГОСТы)
5. Если документация содержит предупреждения — учти их
6. В конце мягко запросить недостающие данные: {", ".join(missing_optional) if missing_optional else "нет"}

Ответ должен быть:
- логичным
- технически корректным
- 5-8 предложений
- без лишних повторов
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Ты опытный инженер техподдержки. Пишешь связно, по делу, без лишнего текста."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=500
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print("Groq error:", e)
            return self._template_fallback(extracted_data)

    # ---------------------------------------------------------
    # 🧠 Очистка документации от мусора
    # ---------------------------------------------------------

    def _clean_documentation(self, docs_context):

        if not docs_context:
            return "Документация не найдена."

        cleaned_chunks = []

        for chunk in docs_context:
            # убираем мусор
            chunk = chunk.replace("\n", " ")
            chunk = chunk.replace("Рисунок", "")
            chunk = chunk.replace("ГОСТ", "")
            chunk = chunk.replace("http://", "")
            chunk = chunk.replace("www.", "")
            chunk = " ".join(chunk.split())

            # отбрасываем слишком короткие или мусорные куски
            if len(chunk) > 100:
                cleaned_chunks.append(chunk)

        return "\n\n".join(cleaned_chunks[:3])  # максимум 3 блока

    # ---------------------------------------------------------
    # 📌 Если нет device_type
    # ---------------------------------------------------------

    def _request_device_type(self, extracted_data):

        return (
            "Благодарим за обращение. "
            "Для предоставления технических рекомендаций необходимо указать точную модель и тип прибора. "
            "После получения этой информации мы сможем предоставить рекомендации согласно официальной документации."
        )

    # ---------------------------------------------------------
    # 🔄 Fallback
    # ---------------------------------------------------------

    def _template_fallback(self, extracted_data):

        return (
            "Ваш запрос получен. "
            "Рекомендуем проверить корректность подключения устройства и его параметры питания. "
            "Если проблема сохраняется, просим сообщить модель прибора и заводской номер для детальной диагностики."
        )