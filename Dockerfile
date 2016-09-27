FROM alpine:3.4
MAINTAINER Ecometrica <>

ENV LANG C

RUN apk add --no-cache bash git mercurial python py-pip openssh

RUN pip install requests==2.8.1

ADD scripts/ /opt/resource/
