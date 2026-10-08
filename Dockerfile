FROM python:3.11-slim

# Hugging Face Spaces runs containers as user 1000
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PORT=7860

WORKDIR /app
COPY --chown=user backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir --user -r backend/requirements.txt

COPY --chown=user backend backend
COPY --chown=user frontend frontend

WORKDIR /app/backend
EXPOSE 7860
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
