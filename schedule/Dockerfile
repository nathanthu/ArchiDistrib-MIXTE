FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY schedule/ .

CMD ["python", "-u", "schedule.py"]
