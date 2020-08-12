FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /Attendance
WORKDIR Attendance
ADD requirements.txt /Attendance
RUN pip3 install -r requirements.txt
ADD . /Attendance/