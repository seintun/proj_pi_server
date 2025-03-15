# Build stage
FROM python:3.9-slim-bullseye as builder

# Set environment variables for build
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    pkg-config \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    gcc \
    libc6-dev \
    libatlas-base-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.9-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONPATH=/app

# Set resource limits for Raspberry Pi
ENV GUNICORN_CMD_ARGS="--workers=1 --threads=2 --worker-class=gthread --timeout 120 --max-requests 1000 --max-requests-jitter 50 --worker-tmp-dir /dev/shm"

# Install minimal runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    procps \
    curl \
    v4l-utils \
    && rm -rf /var/lib/apt/lists/* \
    && echo "vm.overcommit_memory=1" >> /etc/sysctl.conf \
    && echo "vm.swappiness=10" >> /etc/sysctl.conf \
    && echo "vm.dirty_ratio=10" >> /etc/sysctl.conf

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory and create data directory
WORKDIR /app
RUN mkdir -p /app/data

# Copy application files
COPY app.py .
COPY modules/ modules/
COPY static/ static/
COPY templates/ templates/

# Create and configure non-root user
RUN useradd -m -r -u 1000 appuser && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app && \
    chown -R appuser:appuser /app/data

# Create volume for persistent data
VOLUME ["/app/data"]

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Configure resource limits
ENV MEMORY_LIMIT="800M" \
    CPU_LIMIT="1"

# Health check with reduced frequency for lower resource usage
HEALTHCHECK --interval=60s --timeout=30s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the application with optimized Gunicorn settings
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()", "--preload"]
