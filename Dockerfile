# FROM alpine:latest

# RUN apk python3-dev
# RUN pip3 install --no-cache-dir --upgrade pip
FROM ubuntu:18.04


LABEL maintainer="Mahesh <mahesh.baravkar@cuelogic.com>"


RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev



WORKDIR /app
COPY . /app
RUN pip3 install --no-cache-dir --upgrade setuptools
RUN pip3 --no-cache-dir install -r requirements.txt

ENTRYPOINT [ "python3" ]
CMD [ "run.py" ]