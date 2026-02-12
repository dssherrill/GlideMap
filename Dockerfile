# Dockerfile for Glide Range Map - Python Dash Version
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user and group
ARG UID=1000
ARG GID=1000
RUN groupadd -g ${GID} appgroup && \
    useradd -u ${UID} -g appgroup -s /bin/sh -M appuser

# Copy application files
COPY app.py .
COPY Sterling*.cup .

# Ensure the non-root user owns the workdir and all copied files
RUN chown -R appuser:appgroup /app

# Expose the port
EXPOSE 8050

# Set environment variables
ENV DASH_DEBUG_MODE=False

# Switch to non-root user
USER appuser

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:server"]
