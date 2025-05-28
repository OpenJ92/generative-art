FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy clean requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your source files
COPY . .

# Start an interactive shell by default
CMD ["bash"]
