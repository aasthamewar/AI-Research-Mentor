# 1. Use a clean, light Python base image
FROM python:3.10-slim

# 2. Install essential system utilities
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 3. Pull the official Ollama binary straight from their core image
COPY --from=ollama/ollama:latest /usr/bin/ollama /usr/bin/ollama
COPY --from=ollama/ollama:latest /usr/lib/ollama /usr/lib/ollama

# 4. Create a non-root user for Hugging Face compatibility and set up the workspace
RUN useradd -m -u 1000 user
WORKDIR /app

# 5. Handle Python library dependencies (helps with build caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy application files and hand over ownership to the non-root user
COPY --chown=user . .

# 7. FIX: Make entrypoint executable WHILE STILL ROOT before switching users
RUN chmod +x entrypoint.sh

# 8. Switch to the non-root user context
USER user

# 9. Configure ports and runtime environment variables
EXPOSE 7860
ENV OLLAMA_HOST=127.0.0.1:11434
ENV OLLAMA_KEEP_ALIVE=-1
ENV OLLAMA_NUM_PARALLEL=1
ENV OLLAMA_MAX_LOADED_MODELS=1
ENV HOME=/tmp

# 10. Pass control to the entrypoint script
ENTRYPOINT ["./entrypoint.sh"]