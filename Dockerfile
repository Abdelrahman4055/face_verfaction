FROM python:3.11

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libxcb1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# تحميل موديل ArcFace أثناء البناء مش وقت الطلب
RUN python -c "from deepface import DeepFace; DeepFace.build_model('ArcFace')"

COPY . .

CMD ["sh", "-c", "uvicorn Main_Test:app --host 0.0.0.0 --port ${PORT:-8000}"]
