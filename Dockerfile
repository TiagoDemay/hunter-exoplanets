# Dockerfile for the docker image Exoplanet
# Author: Licia Sales & Tiago Demay
# Date: 2022-03-28
# Version: 1.0
# Insper University  

FROM ubuntu:18.04
LABEL "maintainer": "Licia Sales & Tiago Demay"
LABEL "version": "1.0"
LABEL "description": "Exoplanet"

# Install packages

RUN apt update && apt upgrade -y && DEBIAN_FRONTEND=noninteractive apt install -y build-essential  libssl-dev python3.8 \
    python3-pip libbz2-dev libssl-dev libreadline-dev \
    libffi-dev libsqlite3-dev tk-dev libpng-dev libfreetype6-dev llvm-9 llvm-9-dev \
    gfortran gcc locales python3-tk libpython3.8-dev

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV LLVM_CONFIG=/usr/bin/llvm-config-9

#install python3.8 and sherlockpipe

RUN python3 -m pip install pip -U
RUN python3 -m pip install setuptools -U
RUN python3 -m pip install Cython
RUN python3 -m pip install numpy
RUN python3 -m pip install sherlockpipe --pre --ignore-installed PyYAML

# Copy the files for container

COPY $HOME/HunterExoplanets /home
WORKDIR /home

#CMD ["/bin/bash"]
CMD ["time python3 -m sherlockpipe --properties properties.yaml > output.txt"]


 