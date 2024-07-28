FROM python:3.9

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    apt-transport-https \
    ca-certificates \
    software-properties-common \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxkbcommon-x11-0 \
    libgtk-3-0 \
    libgbm-dev \
    libasound2

# Install Node.js for Playwright
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs

# Install Playwright and its dependencies
RUN pip install playwright

# Install Playwright dependencies
RUN playwright install-deps

# Install Playwright browsers
RUN playwright install

# Define working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy application files
COPY . .

# Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]

