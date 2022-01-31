FROM python:3.9-slim-buster

LABEL maintainer="RomainTL"

RUN apt-get update; \
    apt-get -y upgrade; \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY free2move-py/ /tmp/free2move-py/

WORKDIR /tmp/free2move-py/
RUN python setup.py sdist
RUN pip install dist/free2move-1.0.0.tar.gz

WORKDIR /tmp/

ENTRYPOINT ["tail", "-f", "/dev/null"]
