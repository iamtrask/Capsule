FROM openmined/pysyft:edge

WORKDIR /Capsule

COPY . /Capsule

WORKDIR /Capsule
RUN ["pip3", "install", "-r", "requirements.txt"]
RUN ["python3", "setup.py", "install"]
EXPOSE 5002
RUN chmod +x build_and_run_zmq.sh
CMD ["python3","capsule_zmq/local_server.py"]
