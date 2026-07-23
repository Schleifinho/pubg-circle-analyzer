FROM python:3.9
LABEL authors="markus"

WORKDIR /app

# Install OpenCV dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure config files are accessible
VOLUME ["/app/config"]

# Default command (you can override it when running the container)
CMD ["python", "main.py"]
