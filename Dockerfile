FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# إعطاء صلاحيات للكتابة ومسح الملفات المؤقتة
RUN chmod -R 777 /app

EXPOSE 7860

CMD ["gunicorn", "-b", "0.0.0.0:7860", "--timeout", "120", "app:app"]
