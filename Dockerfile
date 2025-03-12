FROM python:3.9-slim

WORKDIR /app

# Add debugging steps
RUN python --version
RUN pip --version

# Install system dependencies for WeasyPrint 64.1
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    python3-cffi \
    python3-brotli \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    libffi-dev \
    libjpeg-dev \
    libopenjp2-7-dev \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    shared-mime-info \
    mime-support \
    gcc \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

# Debug: Show contents of current directory
RUN ls -la

# Copy and show requirements
COPY requirements.txt .
RUN echo "=== Contents of requirements.txt ===" && \
    cat requirements.txt && \
    echo "=== End of requirements.txt ==="

# Update pip first
RUN pip install --no-cache-dir --upgrade pip

# Install packages with verbose output
RUN pip install --no-cache-dir -v -r requirements.txt

# Copy application code
COPY scripts /app/scripts

# Show final structure
RUN echo "=== Final directory structure ===" && \
    ls -R && \
    echo "=== End of directory structure ==="

# Create data directory
RUN mkdir -p /app/data && chmod 777 /app/data

# Default command
CMD ["python", "-u", "scripts/pdfgeneration.py"]
