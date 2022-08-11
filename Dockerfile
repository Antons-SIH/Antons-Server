FROM python:3.8-slim-buster

RUN mkdir /antons

WORKDIR /antons

COPY requirements.txt /antons

RUN apt-get update

RUN yes | apt-get install python3-pip

RUN yes | apt install python3-dev libpq-dev

RUN yes | pip3 install psycopg2

RUN pip3 install -r requirements.txt

COPY . /antons

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0" ]