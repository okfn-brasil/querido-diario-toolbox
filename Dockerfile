FROM python:3.8

RUN adduser --system gazette

RUN apt-get update -y
RUN apt-get -y install default-jre wait-for-it

RUN mkdir /mnt/code
COPY . /mnt/code
WORKDIR /mnt/code
ENV PYTHONPATH=/mnt/code

RUN pip install --no-cache-dir -r requirements.txt

# install Apache Tika
ADD http://archive.apache.org/dist/tika/tika-app-1.24.jar /tika-app.jar
RUN chmod 755 /tika-app.jar 

USER gazette

