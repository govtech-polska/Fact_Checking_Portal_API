FROM python:3.7
RUN mkdir /app && \
    apt-get update
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 8000
COPY ./start_prod.sh /app/
ENTRYPOINT ["/app/start_prod.sh"]
