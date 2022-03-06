FROM ubuntu:20.04

LABEL version="0.1"

ARG DEBIAN_FRONTEND=noninteractive

ENV OPENCV_VERSION="4.0.1"

# Update packages and install basics
RUN apt-get update && apt-get install -y \
	wget \
	unzip \
	git

# Install dependencies
RUN apt-get install -y \
        python3-pip \
        python3-opencv

WORKDIR /var/www
ADD . /var/www/

RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh