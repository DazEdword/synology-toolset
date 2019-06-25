FROM python:3

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt
COPY install-bats.sh install-bats.sh

RUN pip3 --no-cache-dir install -r requirements-dev.txt
RUN ./install-bats.sh

COPY docker/scripts docker/scripts

VOLUME /app
WORKDIR /app
