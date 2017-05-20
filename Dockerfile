FROM alpine:latest

MAINTAINER Patrick Pokatilo <docker-hub@shyxormz.net>

RUN apk update --no-progress && \
    apk add --no-progress \
        py-pip \
        git \
        mercurial && \
    pip install requests

ADD scripts/ /opt/resource/
