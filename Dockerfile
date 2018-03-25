FROM python:2.7

RUN apt-get update && apt-get install -y mysql-client

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
COPY schema.sql /usr/src/app/
RUN pip install -r requirements.txt

EXPOSE 8888

CMD python app.py --mysql_host=mysql
