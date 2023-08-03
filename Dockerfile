FROM python:3.10-alpine
RUN apk add build-base alpine-sdk tk-dev
RUN apk update && apk add mariadb-dev gcc musl-dev python3-dev libffi-dev openssl-dev g++
WORKDIR /password_generator
COPY . /password_generator
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
