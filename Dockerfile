FROM ubuntu:18.04

LABEL maintainer="cdchushig <cdavid.chushig@gmail.com>"

RUN apt-get update && apt-get install -y \
	python3-opencv ca-certificates python3-dev git wget sudo curl && \
  rm -rf /var/lib/apt/lists/*

RUN apt-get install -y \
    python-pip

# create a non-root user
ARG USER_ID=1000
RUN useradd -m --no-log-init --system  --uid ${USER_ID} appuser -g sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER appuser
WORKDIR /home/appuser

ENV PATH="/home/appuser/.local/bin:${PATH}"

RUN pip install --user 'git+https://github.com/facebookresearch/fvcore'
RUN git clone https://github.com/facebookresearch/detectron2 detectron2_repo
RUN pip install --user -e detectron2_repo

COPY requirements.txt /home/appuser/detectron2_repo
RUN pip install --user -r /home/appuser/detectron2_repo/requirements.txt
RUN pip install --user 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'

# Set a fixed model cache directory.
ENV FVCORE_CACHE="/tmp"
WORKDIR /home/appuser/detectron2_repo
ENV PILLOW_VERSION=7.0.0

COPY . /home/appuser/detectron2_repo

# Make port 8080 available to the world outside the container
ENV PORT 8080
EXPOSE 8080

CMD ["python", "app.py"]