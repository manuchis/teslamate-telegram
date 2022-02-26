# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:2.7

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# install the OS build deps
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-dev \
    python3-pip \
    openssl \
    cargo \
    && \
    apt-get clean && \
 && rm -rf /var/lib/apt/lists/*

# Update pip and install pip requirements
RUN python -m pip install --upgrade pip
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
ADD . /app

# The entrypoint translates the variables from the environment into a config file to be read from python
# I did this to avoid modifying the original python app
#COPY ./entrypoint.sh /
#RUN chmod +x /entrypoint.sh
#RUN /entrypoint.sh

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /app
USER appuser



# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "./teslamateMqttToTelegram.py"]
