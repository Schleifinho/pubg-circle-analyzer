FROM ubuntu:latest
LABEL authors="markus"

FROM python:3.9

WORKDIR /app

# Install OpenCV dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure config files are accessible
VOLUME ["/app/config"]

# Default command (you can override it when running the container)
CMD ["python", "main.py"]
