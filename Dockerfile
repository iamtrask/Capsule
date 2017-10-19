FROM openmined/pysyft:edge

WORKDIR /Capsule

COPY . /Capsule

WORKDIR /Capsule
RUN ["pip3", "install", "-r", "requirements.txt"]
RUN ["python3", "setup.py", "install"]
EXPOSE 5002
WORKDIR capsule_zmq
CMD ["python3","local_server.py"]
