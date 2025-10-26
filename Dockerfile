# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create static directory if it doesn't exist
RUN mkdir -p static

# Generate charts
RUN python plot_charts.py

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Create startup script
RUN echo '#!/bin/bash\n\
echo "🚀 Starting application..."\n\
echo "📁 Working directory: $(pwd)"\n\
echo "📋 Files: $(ls -la)"\n\
echo "🐍 Python version: $(python --version)"\n\
echo "📦 Installed packages: $(pip list | grep -E "(Flask|pandas|scikit-learn)")"\n\
echo "🌐 Starting gunicorn..."\n\
exec gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 120 --access-logfile - --error-logfile - app:app' > /app/start.sh && chmod +x /app/start.sh

# Run the application
CMD ["/app/start.sh"]
