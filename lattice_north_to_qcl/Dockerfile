# Use a Python base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Install basic utilities
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    apt-utils \
    curl \
    gnupg \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Redis
RUN apt-get update -y  && apt-get install -y --no-install-recommends redis-server \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install MongoDB client tools
RUN apt-get update && apt-get install -y gnupg && \
    wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add - && \
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-5.0.list && \
    apt-get update && apt-get install -y mongodb-org-tools

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application files to the container
COPY . /app/

# Expose the ports used by the services
EXPOSE 8001 6001

# Start api server with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
