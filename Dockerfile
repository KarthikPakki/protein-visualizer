# Dockerfile
FROM python:3.10-slim

# Install system deps
RUN apt update && apt install -y git curl build-essential

# Set working directory
WORKDIR /app

# Copy app files
COPY . .

# Install all required packages
RUN pip install --no-cache-dir \
    streamlit biopython py3Dmol torch torchvision torchaudio \
    accelerate einops transformers google-generativeai

# Expose Streamlit default port
EXPOSE 8501

# Start the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
