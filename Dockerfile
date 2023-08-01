FROM python:alpine

COPY ./requirements.txt /project/requirements.txt

RUN pip3 install -r /project/requirements.txt

COPY src /app/

WORKDIR /app

CMD [ "python", "main.py"]