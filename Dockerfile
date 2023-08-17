# syntax=docker/dockerfile:1

FROM python:3.9-slim
COPY requirements.txt  /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r requirements.txt
COPY . /opt/app
CMD ["python", "./main.py"]
