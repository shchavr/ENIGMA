import re

from groq import Groq

from app.config import AI_TOKEN


class ExtractionService:
    def __init__(self):
        self.client = Groq(
            api_key=AI_TOKEN
        )

        self.model = "llama-3.3-70b-versatile"

        self._test_connection()

    def _test_connection(self):
        """Тест подключения к Groq"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1
            )
            print(f"✅ Groq подключен успешно (модель: {self.model})")
        except Exception as e:
            print(f"⚠️ Groq не работает: {e}")
            print("  Будет использоваться локальный анализатор")

    def extract_phone(self, text: str):
        match = re.search(r'\+?\d[\d\-\(\) ]{7,}\d', text)
        return match.group(0) if match else None

    def extract_name(self, text: str):
        match = re.search(r'[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+', text)
        return match.group(0) if match else None

    def extract_date(self, text: str):
        match = re.search(r'\b\d{2}\.\d{2}\.\d{4}\b', text)
        return match.group(0) if match else None

    def extract_object(self, text: str):
        match = re.search(r'(ООО|ЗАО|АО|ПАО) «[^»]+»', text)
        return match.group(0) if match else None

    def extract_factory_number(self, text: str):
        match = re.search(r'(Заводской номер|Serial Number|S/N)[:\s]*([A-Za-z0-9\-]+)', text, re.IGNORECASE)
        return match.group(2) if match else None

    def extract_device_type(self, text: str):
        """Улучшенное извлечение типа устройства"""
        device_patterns = [
            r'(контроллер|датчик|прибор|PLC|модуль|блок)\s+([A-Za-zА-Яа-я0-9\-\s]+?)(?:\s+перестал|\s+не\s+работает|\.|,|$)',
            r'([A-Za-z0-9\-]+\s+(?:S7-1200|Siemens|Schneider|Omron|Mitsubishi))',
            r'(Siemens|Schneider|Omron|Mitsubishi|ABB)\s+([A-Za-z0-9\-]+)',
        ]

        for pattern in device_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                device = match.group(0).strip()
                device = re.split(r'\b(перестал|не работает|сломался|требую|прошу)\b', device, flags=re.IGNORECASE)[
                    0].strip()
                return device

        pattern = r'\b(датчик|прибор|контроллер|PLC)\b[\s:–-]*([A-Za-zА-Яа-я0-9\-\s]+)'
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            dt = " ".join(matches[0]).strip()
            dt = re.split(r'\b(Дата|ФИО|Телефон|Email|Объект|Заводской номер)\b', dt)[0].strip()
            return dt
        return None

    def extract_emotion(self, sentiment_label: str):
        mapping = {"POSITIVE": "позитивное", "NEGATIVE": "негативное", "NEUTRAL": "нейтральное"}
        return mapping.get(sentiment_label.upper(), "неопределено")

    def clean_text(self, text: str):
        """Заменяет мат на пробелы (удаляет полностью)"""
        bad_words = ["блять", "хуя", "ебало", "нихуя", "сука", "пиздец", "хуй", "нахуй", "похуй", "хули"]
        pattern = r'\b(' + "|".join(bad_words) + r')\b'
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def extract_summary(self, text: str):
        """Извлекает краткую суть письма с помощью Groq"""

        prompt = f"""Сделай краткую выжимку текста (2 предложения). Убери мат, эмоции, оскорбления. Оставь только суть: проблема, оборудование, что требует клиент.

Текст: {text}

Краткая выжимка (только факты):"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system",
                     "content": "Ты делаешь краткие выжимки текста. Только факты, без эмоций и мата."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=100
            )

            summary = response.choices[0].message.content.strip()

            if len(summary) < 10:
                return self._simple_fallback(text)

            return summary

        except Exception as e:
            print(f"[Groq summary failed] {e}")
            return self._simple_fallback(text)

    def _simple_fallback(self, text: str):
        """Простой локальный анализатор, когда Groq недоступен"""
        text = self.clean_text(text)

        sentences = re.split(r'[.!?]\s+', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s) > 10]

        if not sentences:
            return "Не удалось извлечь суть сообщения"

        important = []
        keywords = ['не работает', 'сломался', 'прибор', 'контроллер', 'ждать', 'горячая линия', 'проблема']

        for s in sentences:
            if any(k in s.lower() for k in keywords):
                important.append(s)

        if important:
            summary = ". ".join(important[:2])
        else:
            summary = ". ".join(sentences[:2])

        if not summary.endswith('.'):
            summary += '.'

        return summary

    def extract_all(self, text: str, sentiment_label: str):
        """Извлекает все данные из текста"""
        # Извлекаем email
        email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
        email = email_match.group(0) if email_match else None

        result = {
            "date": self.extract_date(text),
            "full_name": self.extract_name(text),
            "object": self.extract_object(text),
            "phone": self.extract_phone(text),
            "email": email,
            "factory_number": self.extract_factory_number(text),
            "device_type": self.extract_device_type(text),
            "emotion": self.extract_emotion(sentiment_label),
            "summary": self.extract_summary(text)
        }
        return result
