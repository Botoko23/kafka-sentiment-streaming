FROM python:3.9-slim

# Install dependencies, including netcat-openbsd
RUN apt-get update && apt-get install -y netcat-openbsd

WORKDIR /app
# Install dependencies
COPY . /app

RUN pip install -r requirements.txt

RUN chmod +x wait-for-kafka.sh

# Entry point
ENTRYPOINT ["./wait-for-kafka.sh", "python", "producer.py"]
