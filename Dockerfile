FROM python:3.8.8

COPY ./app/requirements.txt /requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r /requirements.txt

RUN groupadd -r forecast && useradd -r -g forecast forecast
COPY ./app /app
RUN chown -R forecast /app
WORKDIR /app
