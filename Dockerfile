FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV NOTES_FILE=/data/notes.txt
ENV PORT=5000

VOLUME ["/data"]
EXPOSE 5000

CMD ["python", "app.py"]
