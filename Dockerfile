FROM python:3.12-alpine

RUN apk add --no-cache bash

COPY services /services

RUN pip3 install -r /services/requirements.txt

COPY assets/wait_for_mq.sh /usr/bin/wait_for_mq.sh
COPY assets/image-reader /usr/bin/image-reader
COPY assets/image-processor /usr/bin/image-processor
COPY assets/image-triager /usr/bin/image-triager
