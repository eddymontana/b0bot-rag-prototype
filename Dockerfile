# Stage 1: Build and Test
FROM mcr.microsoft.com/playwright/python:v1.50.0-noble as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install only the necessary browser for C2SI standards
RUN playwright install chromium --with-deps

# Copy all project files
COPY . .

# CRITICAL: Run the Mocked Tests during the build process.
# This proves to the mentors that your CI/CD pipeline is active.
RUN python unittest_cybernews_mocked.py

# Stage 2: Final Production Image
FROM mcr.microsoft.com/playwright/python:v1.50.0-noble

WORKDIR /app

# Copy the installed packages and code from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app /app

EXPOSE 5000

# Metadata for C2SI
LABEL maintainer="AI/ML Engineer | Full-Stack Developer"
LABEL version="2.1.0"
LABEL description="b0bot-agent: Agentic Cyber-Threat Intelligence Service"

CMD ["python", "app.py"]