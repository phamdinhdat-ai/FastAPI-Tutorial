FROM ubuntu:22.04




LABEL maintained="datolg123@gmail.com"
LABEL version="1.0"
LABEL decription='This is an example of dockerfile for FastAPI - LLM'
LABEL name="fastapi_llm"


ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update 
RUN apt-get install curl -y
#confirm that have the prerequisites installed
RUN apt-get install -y software-properties-common 
# need PPA. add maintained by deadsnakes
RUN add-apt-repository ppa:deadsnakes/ppa
# RUN apt update
# install python 
RUN apt-get install -y python3.9  
# install package pip for ubunt
RUN apt-get install -y python3-pip 
RUN pip3 install --upgrade pip
RUN apt-get update
RUN apt -y upgrade 


WORKDIR /fastapi_llm

COPY ./api /fastapi_llm

COPY ./requirements.txt /fastapi_llm

RUN pip install -r /fastapi_llm/requirements.txt


ENV HF_TOKEN="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"
ENV HF_EMBEDDING="BAAI/bge-small-en-v1.5"
ENV HF_REPO_ID="mistralai/Mistral-7B-Instruct-v0.3"


