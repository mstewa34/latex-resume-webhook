FROM python:alpine

RUN apk --update add git openssh && \
    rm -rf /var/lib/apt/lists/* && \
	    rm /var/cache/apk/*

RUN pip install flask flask-limiter docker

COPY ./server.py /app/
WORKDIR /app

ENTRYPOINT ["python"]
CMD ["server.py"]
