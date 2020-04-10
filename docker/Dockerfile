FROM python:3.6

ENV PYTHONPATH="$PYTHONPATH:/app"

RUN pip install --upgrade pip
RUN pip install pipenv

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
COPY install-bats.sh install-bats.sh
COPY install-bats-core.sh install-bats-core.sh

ARG SSH_KEY_NAME

RUN echo "IdentityFile ~/.ssh/$SSH_KEY_NAME" >> /etc/ssh/ssh_config

COPY .env.tests /root/.synotools/credentials

RUN pipenv install --system --dev --pre
RUN git clone https://github.com/bats-core/bats-core.git && cd bats-core && ./install.sh /usr/local

COPY docker/scripts docker/scripts
COPY synotools synotools

VOLUME /app
WORKDIR /app
