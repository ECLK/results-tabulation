# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
FROM python:3.6

ENV TZ=Asia/Colombo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir /app
WORKDIR /app
ADD . /app

# Install requirements
RUN pip install -r requirements.txt
RUN export ENV_CONFIG=./env/dev.cfg

CMD [ "python", "excecute_mysql_query.py", "./env/dev.cfg", "./parliament-election-2020/create-or-update-counting-dashboard-tables.sql" ]
