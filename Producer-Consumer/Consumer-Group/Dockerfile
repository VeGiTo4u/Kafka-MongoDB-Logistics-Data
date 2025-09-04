# Use an official Python runtime as a parent image
FROM python:3.12-slim
# Set working directory
WORKDIR /app
# Install system dependencies for SSL and building packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libssl-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*
# Copy current directory into container
COPY . /app
# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir confluent-kafka pymongo requests fastavro attrs httpx cachetools authlib certifi
# Set environment variable for certifi (ensures MongoDB SSL works)
ENV SSL_CERT_FILE=/usr/local/lib/python3.12/site-packages/certifi/cacert.pem
# Expose a port if needed (optional)
EXPOSE 80
# Run the consumer script
CMD ["python3", "consumer.py"]
