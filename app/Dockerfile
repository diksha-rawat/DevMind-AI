# Use Python 3.11 as our base image
# slim = smaller image size, faster to build
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first
# Docker caches this layer — so if requirements don't change
# it won't reinstall packages every time you build
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY main.py .

# Tell Docker our app runs on port 8080
EXPOSE 8080

# Health check — Kubernetes uses this to know if app is alive
HEALTHCHECK --interval=30s --timeout=5s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"

# Command to run the app
CMD ["python", "main.py"]
