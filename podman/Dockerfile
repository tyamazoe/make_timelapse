FROM python:3-slim-bookworm

# Install ffmpeg and other dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir boto3 pillow

# Set working directory
WORKDIR /app

# Copy application files
COPY make_timelapse.py /app/
COPY arialn.ttf /app/

# Create directories for mounting
RUN mkdir -p /app/work /root/.aws

# ENTRYPOINT ["python3", "make_timelapse.py"]
CMD ["/bin/bash"]
