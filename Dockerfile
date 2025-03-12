FROM python:3.9

WORKDIR /app

RUN pip install watchdog minio python-dotenv kafka-python

COPY scripts /app/scripts

# Default command set in docker-compose.yml
CMD ["python", "-u", "scripts/miniotokafka.py"]