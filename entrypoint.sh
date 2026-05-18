#!/bin/bash

# Start the Ollama background engine process
ollama serve &

# Block until Ollama is responsive on its default internal port
until curl -s http://127.0.0.1:11434 > /dev/null; do
  echo "Waiting for local Ollama engine to wake up..."
  sleep 3
done

# Pull down the model weights internally
echo "Downloading Llama 3.2 1B model..."
ollama pull llama3.2:1b

# Launch your public-facing FastAPI server on port 7860
echo "Launching FastAPI Engine..."
exec uvicorn api:app --host 0.0.0.0 --port 7860