FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r /app/requirements.txt

RUN pip3 install --no-cache-dir gunicorn

COPY main.py .

CMD [ "gunicorn", "-w", "2", "-b", "0.0.0.0", "main:APP" ]
