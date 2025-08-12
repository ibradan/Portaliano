# Multi-stage Dockerfile for Portaliano Automation
# Ultra-minimal size with browser_config integration
FROM python:3.10-slim as builder

# Set environment variables for optimization
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install minimal runtime dependencies for Playwright + Flask
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Essential for Playwright Chromium (minimal set)
    libnss3 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libxss1 \
    libasound2 \
    # Essential for Flask app
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && apt-get autoremove -y \
    && apt-get autoclean

# Set working directory
WORKDIR /app

# Copy and install Python dependencies (separate layer for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip cache purge

# Install only Chromium browser (not all browsers) to save 400MB+
RUN playwright install chromium \
    && playwright install-deps chromium \
    && rm -rf /tmp/* /var/tmp/*

# ========================= 
# Production Stage (minimal)
# =========================
FROM python:3.10-slim as production

# Copy runtime libraries from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /ms-playwright /ms-playwright

# Install only essential runtime dependencies (no build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 libatk-bridge2.0-0 libdrm2 libxkbcommon0 \
    libxcomposite1 libxdamage1 libxrandr2 libgbm1 \
    libxss1 libasound2 curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && apt-get autoremove -y

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN useradd -m -u 1000 appuser \
    && chown -R appuser:appuser /app

# Copy application code (minimal set only)
COPY --chown=appuser:appuser app.py browser_config.py ./
COPY --chown=appuser:appuser *.csv ./
COPY --chown=appuser:appuser static/ ./static/
COPY --chown=appuser:appuser templates/ ./templates/

# Switch to non-root user
USER appuser

# Create required directories
RUN mkdir -p uploads logs

# Set environment variables for production headless mode
ENV FLASK_APP=app.py \
    FLASK_ENV=production \
    PORT=5000

# Expose Flask port
EXPOSE 5000

# Health check (lightweight)
HEALTHCHECK --interval=60s --timeout=10s --start-period=90s --retries=2 \
    CMD curl -f http://localhost:5000/dashboard || exit 1

# Start command (production ready with browser_config)
CMD ["python3", "app.py"]
