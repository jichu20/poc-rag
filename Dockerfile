# FROM ubuntu:20.04
FROM python:3.9
WORKDIR /app
USER root

RUN useradd -ms /bin/bash admin
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


ARG GRADIO_PORT=7860
ARG LOCATION="eu"
ARG PROJECT_ID=""
ARG PROCESSOR_OCR_ID=""
ARG PROCESSOR_OCR_VERSION=""
ARG SERVER_ADDRESS="0.0.0.0"

# chromaDb server
ARG SERVER_CHROMADB="0.0.0.0"
ARG PORT_CHROMADB=8081

ENV location=$LOCATION
ENV project_id=$PROJECT_ID
ENV processor_ocr_id=$PROCESSOR_OCR_ID
ENV processor_ocr_version=$PROCESSOR_OCR_VERSION
ENV GRADIO_PORT=${GRADIO_PORT}
ENV SERVER_ADDRESS=${SERVER_ADDRESS}
ENV SERVER_CHROMADB=${SERVER_CHROMADB}
ENV PORT_CHROMADB=${PORT_CHROMADB}


COPY . .
EXPOSE 7860


CMD [ "python", "app.py" ]