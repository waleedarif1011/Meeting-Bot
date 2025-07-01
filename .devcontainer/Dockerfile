FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including Node.js for serving frontend
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    vim \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install a simple HTTP server globally for serving static files
RUN npm install -g http-server

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Flask port and frontend port
EXPOSE 5000
EXPOSE 3000

# Set environment variables
ENV FLASK_APP=server.py
ENV FLASK_ENV=development
ENV PYTHONPATH=/app

# Default command (can be overridden)
CMD ["bash"]
