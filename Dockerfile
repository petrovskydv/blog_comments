FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .

ADD . /code/

# run entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]

EXPOSE 8000

