FROM 10.32.42.225:5000/python:3.7-buster
USER root
WORKDIR /usr/src/app

# set timezone
ENV TZ=America/Toronto
ENV HTTP_PROXY="http://proxy.charite.de:8080"
ENV HTTPS_PROXY="http://proxy.charite.de:8080"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update
RUN apt-get install -y vim
RUN apt-get install -y less
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x gunicorn_starter.sh
CMD ["./gunicorn_starter.sh"]
