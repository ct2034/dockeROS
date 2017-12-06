FROM ubuntu:xenial

COPY . /
RUN apt-get update
RUN apt-get install -y python-pip
RUN pip install -r requirements.txt

CMD ['bash', 'run_server.sh']
