FROM python:3
ADD server.py /
ADD SQLModule.py /
RUN pip install MySQLdb
RUN pip install flask
ENTRYPOINT [ "python", "./server.py" ]
