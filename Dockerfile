FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY onet_loader.py .
COPY onet_data/ ./onet_data/
COPY static/ ./static/
COPY templates/ ./templates/

# Expose the default HF Spaces port
EXPOSE 7860

# Run Flask using gunicorn on the port specified by the PORT environment variable
CMD gunicorn --bind 0.0.0.0:${PORT:-10000} app:app
