FROM python:3.9

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up the application environment
WORKDIR /app

# Copy the requirements file and install dependencies
COPY app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app /app

# Expose the IPython port
EXPOSE 8888

# Set the entrypoint to ipython
ENTRYPOINT ["ipython"]
