# Dockerfile for Glide Range Map - Python Dash Version
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY Sterling*.cup .

# Expose the port
EXPOSE 8050

# Set environment variables
ENV DASH_DEBUG_MODE=False

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:server"]
