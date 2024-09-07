# Use a Python 3.10.13 base image for ARM architecture
FROM python:3.10.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive

# Install dependencies (git, curl) to clone the repository and make changes
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    portaudio19-dev \
    libffi-dev \
    libssl-dev \
    libsndfile1 \
    libsndfile1-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Upgrade pip to version 24.0.0
RUN python -m pip install --upgrade pip==24.0.0

# Clone the repository
RUN git clone https://github.com/erew123/alltalk_tts.git /tmp/alltalk_tts && \
    cp -r /tmp/alltalk_tts/* . && \
    rm -rf /tmp/alltalk_tts

# Install Python dependencies
RUN pip install -r /app/system/requirements/requirements_standalone.txt || true

COPY builder/requirements.txt /requirements.txt

RUN pip install -r /requirements.txt --no-cache-dir && rm /requirements.txt

# Add src files (Worker Template)
ADD src .

# Download model
RUN python /modeldownload.py

CMD python -u /handler.py

