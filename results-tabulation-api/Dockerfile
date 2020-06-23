# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
FROM python:3.6

ENV TZ=Asia/Colombo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

LABEL Name=results-tabulation-tallysheets
EXPOSE 5000

RUN mkdir /app
WORKDIR /app
ADD . /app

RUN apt-get update
RUN apt-get install -y apt-utils libpq-dev python-dev
RUN apt-get install -y wkhtmltopdf

# Install requirements
RUN pip install -r requirements.txt
RUN export ENV_CONFIG=./env/dev.cfg
RUN python manage.py create_database; exit 0
RUN python manage.py db upgrade; exit 0

CMD [ "python", "index.py" ]
