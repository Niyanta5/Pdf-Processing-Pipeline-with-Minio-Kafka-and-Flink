import json
import logging
import os
from kafka import KafkaConsumer
from dotenv import load_dotenv

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

def main():
    # Kafka configuration
    bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
    topic = os.getenv('KAFKA_TOPIC', 'minio-events')
    group_id = os.getenv('KAFKA_GROUP_ID', 'minio-metadata-consumer')

    print(f"Starting Kafka consumer...")
    print(f"Bootstrap servers: {bootstrap_servers}")
    print(f"Topic: {topic}")
    print(f"Group ID: {group_id}")

    # Create Kafka consumer
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    print("Consumer created successfully. Waiting for messages...")

    # Consume messages
    try:
        for message in consumer:
            print("\n--- New message received ---")
            print(f"Topic: {message.topic}")
            print(f"Partition: {message.partition}")
            print(f"Offset: {message.offset}")
            print(f"Key: {message.key}")
            print(f"Value: {json.dumps(message.value, indent=2)}")
            print("---------------------------")
    except KeyboardInterrupt:
        print("\nShutting down consumer...")
    finally:
        consumer.close()
        print("Consumer closed.")

if __name__ == "__main__":
    main()