#!/bin/bash

echo "Creating Kafka topic..."
docker exec kafka kafka-topics.sh --create \
    --topic minio-events \
    --bootstrap-server kafka:9092 \
    --partitions 1 \
    --replication-factor 1

echo "Verifying topic creation..."
docker exec kafka kafka-topics.sh --describe \
    --topic minio-events \
    --bootstrap-server kafka:9092