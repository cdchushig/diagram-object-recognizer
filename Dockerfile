FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

# gcc compiler and opencv prerequisites
#RUN apt-get -y install nano git build-essential libglib2.0-0 libsm6 libxext6 libxrender-dev sudo cmake ninja-build
#RUN apt-get -y install libgl1 libgl1-mesa-dev
#RUN apt-get -y install ffmpeg libsm6 libxext6

RUN apt-get update && apt-get install -y \
	ca-certificates python3-pip python3-dev git sudo ninja-build
RUN ln -sv /usr/bin/python3 /usr/bin/python

RUN apt-get install -y python3-opencv

ADD . /home/appuser/

# create a non-root user
ARG USER_ID=1000
RUN useradd -m --no-log-init --system --uid ${USER_ID} appuser -g sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN chown appuser -R /home/appuser

USER appuser
WORKDIR /home/appuser

ENV PATH="/home/appuser/.local/bin:${PATH}"

# Detectron2 prerequisites
RUN pip install --user tensorboard cmake
RUN pip install --user torch==1.10.1 torchvision==0.11.2 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install --user 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'
RUN pip install --user 'git+https://github.com/facebookresearch/fvcore'
RUN git clone https://github.com/facebookresearch/detectron2 detectron2_repo
RUN pip install --user -e detectron2_repo
RUN pip install -r requirements_prod.txt

RUN chmod 777 /home/appuser/uploads

EXPOSE 5000
