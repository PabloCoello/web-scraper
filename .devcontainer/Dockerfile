FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
                git \
                cmake \
                software-properties-common \
                python3.8 \
                python3-pip \
                wget \
                firefox

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
RUN tar -xvzf geckodriver* 
RUN chmod +x geckodriver
RUN mv geckodriver /usr/local/bin/

RUN python3 -m pip install pandas \
                        selenium \
                        openpyxl

RUN apt-get update

RUN mkdir -p /local/lib/python3.8/dist-packages/

ENV PYTHONPATH=/local/lib/python3.8/dist-packages/

WORKDIR /opt/web-scraper/