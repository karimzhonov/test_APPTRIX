FROM python:3.9

RUN apt update && apt install postgresql -y
RUN apt install libsm6 libxrender1 libfontconfig1 libice6 -y

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN python manage.py migrate