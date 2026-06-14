FROM python:3.12-slim

WORKDIR /app

RUN python -m pip install --upgrade pip setuptools wheel

COPY pyproject.toml requirements.txt README.md Procfile ./
COPY src ./src
COPY app.py ./

RUN python -m pip install -r requirements.txt
RUN python -m pip install .

EXPOSE 7860
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-7860}"]
