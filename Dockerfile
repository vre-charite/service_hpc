FROM 10.32.42.225:5000/python:3.7-buster
USER root
WORKDIR /usr/src/app

# set timezone
ENV TZ=America/Toronto
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update -y
RUN apt-get install vim less -y
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x gunicorn_starter.sh
CMD ["./gunicorn_starter.sh"]
