FROM python:3.10.4-slim-buster

COPY . /app/

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt -i "https://mirrors.aliyun.com/pypi/simple/" \
    && pip install pycryptodome \
    && mkdir -p /app/runtime/logs && touch /app/runtime/logs/Task.log \
    && ln -sfT /dev/stdout /app/runtime/logs/Task.log

# on start up
CMD cd /app && python3.10 ./test_alive.py \
   && python3.10 ./main.py

EXPOSE 5050