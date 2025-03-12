#!/bin/bash
# Quick system test
echo "Testing system components..."

# 1. Generate a PDF
echo "test content" > /tmp/test.pdf
docker cp /tmp/test.pdf minio-server:/data/
docker exec minio-server mc cp /data/test.pdf myminio/mybucket/

# 2. Monitor events
docker exec kafka kafka-console-consumer.sh \
    --bootstrap-server kafka:9092 \
    --topic minio-events \
    --from-beginning \
    --timeout-ms 10000

# 3. Clean up
rm -f /tmp/test.pdf

