#!/bin/bash

# Create temporary directory
mkdir -p /tmp/minio_files

# Download all existing files from MinIO
echo "Downloading existing files..."
docker exec minio-server mc cp --recursive myminio/mybucket/ /data/
docker cp minio-server:/data/. /tmp/minio_files/

# Remove all files from bucket
echo "Clearing bucket..."
docker exec minio-server mc rm --force --recursive myminio/mybucket

# Re-upload all files to trigger new events
echo "Re-uploading files to trigger events..."
for file in /tmp/minio_files/*; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        echo "Re-uploading $filename..."
        docker cp "$file" minio-server:/data/
        docker exec minio-server mc cp "/data/$filename" myminio/mybucket/
    fi
done

# Clean up
rm -rf /tmp/minio_files

echo "Re-upload complete. Check Kafka events now."