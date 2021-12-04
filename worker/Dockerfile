FROM python:3.8-slim-buster

# System packages installation
RUN apt-get update -y
RUN apt install -y \
    apt-utils \
    curl \
    gnupg2 \
    ca-certificates \
    lsb-release \
    libglib2.0-0 \
    libgtk2.0-dev \
    libsm6 \
    libxext6 \
    libxrender-dev

# API dependecies + config
RUN pip3 install gunicorn==20.0.4

# Copy and install source
COPY ./worker/src/ /opt/worker/

RUN pip3 install -e /opt/worker/

WORKDIR /opt/worker/

EXPOSE 8080

CMD exec gunicorn worker.flask_app:app \
        --bind :$PORT \
        --workers 1 \
        --threads 1 \
        --timeout 3600
