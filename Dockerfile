# 1. Use a clean, light Python base image
FROM python:3.10-slim

# 2. Install essential system utilities
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 3. Pull the official Ollama binary straight from their core image
COPY --from=ollama/ollama:latest /usr/bin/ollama /usr/bin/ollama

# 4. Create and set the workspace directory
WORKDIR /app

# 5. Handle Python library dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy application files into the build context
COPY . .

# 7. Configure ports for Hugging Face Spaces (HF expects port 7860)
EXPOSE 7860
ENV OLLAMA_HOST=127.0.0.1:11434
ENV OLLAMA_KEEP_ALIVE=-1

# 8. Use an entrypoint script to launch Ollama and FastAPI concurrently
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]