FROM python:3

ENV PYTHONPATH="$PYTHONPATH:/app"

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt
COPY install-bats.sh install-bats.sh
COPY install-bats-core.sh install-bats-core.sh

ARG SSH_KEY_NAME

RUN echo "IdentityFile ~/.ssh/$SSH_KEY_NAME" >> /etc/ssh/ssh_config

COPY .env.tests /root/.synotools/credentials

RUN pip3 --no-cache-dir install -r requirements-dev.txt
RUN git clone https://github.com/bats-core/bats-core.git && cd bats-core && ./install.sh /usr/local

COPY docker/scripts docker/scripts
COPY synotools synotools

VOLUME /app
WORKDIR /app
