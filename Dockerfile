# 1. Use the latest stable, slim Python 3.12 (standard for AI in 2026)
FROM python:3.12-slim

# 2. Set environment variables to optimize Python for containers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# 3. Set work directory
WORKDIR /app

# 4. Install system dependencies (Playwright needs these for browser automation)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libnss3 \
    libatk1.0-0 \
    libcups2 \
    libdrm2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libxkbcommon0 \
    libpango-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 5. Create a non-root user for security (Crucial for GSoC approval)
RUN adduser --disabled-password --gecos "" appuser

# 6. Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# 7. Install Python dependencies
RUN pip install -r requirements.txt && \
    playwright install chromium --with-deps

# 8. Copy the rest of the application code
COPY . .

# 9. Switch to the non-root user
USER appuser

# 10. Expose the port your Flask app runs on
EXPOSE 5000

# 11. Start the application
CMD ["python", "main.py"]