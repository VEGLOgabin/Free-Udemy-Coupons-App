# FROM python:3.9

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#   wget \
#   gnupg \
#   unzip \
#   curl \
#   firefox-esr

# # Install Geckodriver
# RUN GECKODRIVER_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/') && \
#     wget -q --continue -P /tmp "https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz" && \
#     tar -xzf /tmp/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz -C /opt && \
#     rm /tmp/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz && \
#     ln -fs /opt/geckodriver /usr/local/bin/geckodriver

# WORKDIR /app

# COPY . .

# RUN pip install -r requirements.txt

# # COPY . .

# # Command to run the Streamlit app : --server.address=0.0.0.0  is for Streamlit Server Address: Ensure Streamlit is configured to listen on all interfaces inside the container. 
# CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]  

FROM python:3.9

# Install system dependencies
RUN apt-get update && apt-get install -y \
  wget \
  gnupg \
  unzip \
  curl \
  firefox-esr

# Install Geckodriver
RUN GECKODRIVER_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/') && \
    wget -q --continue -P /tmp "https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz" && \
    tar -xzf /tmp/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz -C /opt && \
    rm /tmp/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz && \
    ln -fs /opt/geckodriver /usr/local/bin/geckodriver

# Install pip packages
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Command to run the Streamlit app : --server.address=0.0.0.0 is for Streamlit Server Address: Ensure Streamlit is configured to listen on all interfaces inside the container. 
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]






