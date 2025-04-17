FROM python:3.9-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY src/ ./src/

# Set environment variables
ENV PYTHONPATH=/app
ENV MODULE_NAME=src.main
ENV VARIABLE_NAME=app
ENV PORT=8001

# Expose the port
EXPOSE 8001

# Start the application with Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001"] 