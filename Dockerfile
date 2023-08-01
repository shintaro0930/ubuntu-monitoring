FROM ubuntu:22.04

ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y \
    build-essential \
    python3 \
    python3-pip \
    curl \
    sudo


RUN pip3 install -y \
    beautifulsoup4 \
    jpholiday \
    flask \
    flask_cors