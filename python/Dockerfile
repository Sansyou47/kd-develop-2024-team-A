FROM python:3.11
RUN apt update && apt install -y libjpeg-dev build-essential
WORKDIR /usr/local/lib
COPY ./app/function/clib/bit-convert.c .
RUN gcc -shared -O2 -o bit-convert.so bit-convert.c
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#Pythonファイルの実行
CMD ["python", "-u", "app.py"]