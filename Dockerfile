FROM ubuntu:18.04

LABEL maintainer="cdchushig <cdavid.chushig@gmail.com>"

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
	python3-opencv python3-pip python3-dev git wget sudo curl && \
  rm -rf /var/lib/apt/lists/*

# create a non-root user
#ARG USER_ID=1000
#RUN useradd -m --no-log-init --system  --uid ${USER_ID} appuser -g sudo
#RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
#USER appuser
#WORKDIR /home/appuser

#ENV PATH="/home/appuser/.local/bin:${PATH}"

ADD . /code
WORKDIR /code

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN git clone https://github.com/facebookresearch/detectron2 detectron2_repo
RUN pip3 install -e detectron2_repo

ENV PILLOW_VERSION=7.0.0

ENV PORT 8080
EXPOSE 8080

CMD ["python", "app.py"]