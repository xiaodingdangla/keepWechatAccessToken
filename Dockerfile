FROM python:3.12.0-alpine3.18
MAINTAINER "Wangshuzhan"
ADD . /code
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt
WORKDIR /code
ENV TZ=Asia/Shanghai
CMD ["python", "main.py"]
