FROM python:3.8-slim-buster

WORKDIR /app

RUN pip install --upgrade pip

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]
