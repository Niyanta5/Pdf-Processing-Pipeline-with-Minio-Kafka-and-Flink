#!/bin/bash

echo "Creating Kafka topic first..."
docker exec kafka kafka-topics.sh --create \
    --topic minio-events \
    --bootstrap-server kafka:9092 \
    --partitions 1 \
    --replication-factor 1 \
    --if-not-exists

echo "Setting up MinIO bucket and notifications..."
docker exec minio-server mc alias set myminio http://localhost:9000 admin admin@123

echo "Creating bucket..."
docker exec minio-server mc mb --ignore-existing myminio/mybucket

echo "Setting up Kafka notifications..."
# Enable Kafka notifications
docker exec minio-server mc admin config set myminio notify_kafka enable=on

# Configure Kafka notification target
docker exec minio-server mc admin config set myminio notify_kafka:1 \
    brokers="kafka:9092" \
    topic="minio-events" \
    queue_dir="" \
    queue_limit="0" \
    tls_skip_verify="off" \
    tls_client_auth="0" \
    sasl="off" \
    sasl_mechanism="plain" \
    comment="kafka1"

echo "Restarting MinIO server..."
docker restart minio-server

echo "Waiting for MinIO to restart..."
sleep 15

echo "Reconfiguring MinIO alias..."
docker exec minio-server mc alias set myminio http://localhost:9000 admin admin@123

echo "Setting up bucket event notifications..."
# Clear existing notifications
docker exec minio-server mc event remove myminio/mybucket arn:minio:sqs::1:kafka || true

# Add new notifications with explicit event types
docker exec minio-server mc event add myminio/mybucket arn:minio:sqs::1:kafka \
    --event put \
    --event delete \
    --event get \
    --suffix .pdf,.txt

echo "Verifying notifications..."
docker exec minio-server mc event list myminio/mybucket
docker exec minio-server mc admin config get myminio notify_kafka

echo "Testing notification setup..."
# Create and upload a test file
echo "test content" > data/test.pdf
docker cp data/test.pdf minio-server:/data/
docker exec minio-server mc cp /data/test.pdf myminio/mybucket/

echo "Setup complete! Please check Kafka events."

