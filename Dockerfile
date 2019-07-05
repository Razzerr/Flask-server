FROM python:3
ADD server.py /
ADD SQLModule.py /
ADD ServerConstants.py /
ADD ServerInit.py /
RUN pip3 install mysqlclient
RUN pip3 install flask
ENTRYPOINT [ "python3", "./ServerInit.py" ]
