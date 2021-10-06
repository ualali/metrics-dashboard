# Use the official Python image (https://hub.docker.com/_/python).
FROM python:3.7-slim

# Copy local code to the container image.
COPY . /app
WORKDIR /app

# Prometheus exporter vars
ENV PROMETHEUS_MULTIPROC_DIR /app
ENV prometheus_multiproc_dir /app

# Install dependencies.
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Start application server.
CMD ["gunicorn", "--access-logfile", "-", "--error-logfile", "-", "-c", "config.py", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
