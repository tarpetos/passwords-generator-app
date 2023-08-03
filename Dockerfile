FROM python:3.10-alpine
ENV PYTHONUNBUFFERED 1
RUN apk add build-base alpine-sdk tk-dev
WORKDIR /password_generator/
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
