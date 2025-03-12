import json
import logging
import os
import time
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from dotenv import load_dotenv
import socket
from contextlib import contextmanager

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Kafka Consumer Configuration
KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', 'minio-events')
KAFKA_GROUP_ID = os.environ.get('KAFKA_GROUP_ID', 'minio-metadata-consumer')

def process_minio_metadata(metadata):
    """
    Process the Minio metadata received from Kafka.
    Customize this function based on your specific requirements.
    """
    try:
        # Check if this is a MinIO notification
        if 'Records' in metadata:
            for record in metadata.get('Records', []):
                event_name = record.get('eventName', 'unknown')
                bucket_name = record.get('s3', {}).get('bucket', {}).get('name', 'unknown')
                object_key = record.get('s3', {}).get('object', {}).get('key', 'unknown')
                size = record.get('s3', {}).get('object', {}).get('size', 0)
                
                logger.info(f"Event: {event_name}, Bucket: {bucket_name}, Object: {object_key}, Size: {size}")
                
                # Example: Additional processing based on event type
                if 'ObjectCreated' in event_name:
                    logger.info(f"New object created: {object_key}")
                    # Add your custom logic here
                
                elif 'ObjectRemoved' in event_name:
                    logger.info(f"Object removed: {object_key}")
                    # Add your custom logic here
                
                elif 'ObjectAccessed' in event_name:
                    logger.info(f"Object accessed: {object_key}")
                    # Add your custom logic here
        else:
            # Handle non-standard messages
            logger.info(f"Received non-standard message: {metadata}")
            
        return True
    except Exception as e:
        logger.error(f"Error processing metadata: {str(e)}")
        return False

def create_consumer(bootstrap_servers, topic, group_id, max_retries=5, retry_delay=10):
    """Create Kafka consumer with improved retry logic"""
    for attempt in range(max_retries):
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=bootstrap_servers,
                group_id=group_id,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                security_protocol="PLAINTEXT",
                api_version=(0, 10, 2),
                session_timeout_ms=30000,
                heartbeat_interval_ms=10000,
                max_poll_interval_ms=300000,
                request_timeout_ms=305000
            )
            # Test the connection
            consumer.topics()
            return consumer
        except Exception as e:
            if attempt < max_retries - 1:
                logger.error(f"Failed to connect to Kafka (attempt {attempt + 1}/{max_retries}): {e}")
                time.sleep(retry_delay)
            else:
                raise Exception(f"Failed to connect to Kafka after {max_retries} attempts: {e}")

def main():
    while True:
        try:
            consumer = create_consumer(
                KAFKA_BOOTSTRAP_SERVERS,
                KAFKA_TOPIC,
                KAFKA_GROUP_ID
            )
            logger.info("Connected to Kafka successfully")

            for message in consumer:
                try:
                    process_minio_metadata(message.value)
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    continue

        except Exception as e:
            logger.error(f"Consumer error: {e}")
            logger.info("Attempting to reconnect in 10 seconds...")
            time.sleep(10)
        finally:
            try:
                consumer.close()
            except Exception:
                pass

if __name__ == "__main__":
    main()