#!/bin/bash

echo "Restarting MinIO server..."
docker-compose restart minio-server

# Wait for MinIO to restart
echo 'Waiting for MinIO to restart...'
sleep 15

# Configure MinIO client and set Kafka notifications in one container
docker run --rm --network pdftovoiceconverter_app-network \
  --entrypoint /bin/sh \
  minio/mc \
  -c "
    # Configure MinIO client
    mc alias set myminio http://minio-server:9000 admin admin@123
    
    # Configure Kafka notifications
    mc admin config set myminio notify_kafka:1 brokers=kafka:9092 topic=minio-events
    
    # Wait a moment for config to apply
    sleep 5
    
    # Add event notifications for the bucket
    mc mb --ignore-existing myminio/mybucket
    mc event add myminio/mybucket arn:minio:sqs::1:kafka --event put,delete,get
    
    # List event notifications to verify
    echo 'Current event notifications:'
    mc event list myminio/mybucket
  "

echo "Restarting MinIO server again to apply notification config..."
docker-compose restart minio-server

echo "Setup complete! Wait a moment and then try uploading a file to test notifications."