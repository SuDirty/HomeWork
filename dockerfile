FROM python:3.11-slim
WORKDIR /homework
COPY . /homework
RUN export PYTHONWARNINGS='ignore:resource_tracker:UserWarning'