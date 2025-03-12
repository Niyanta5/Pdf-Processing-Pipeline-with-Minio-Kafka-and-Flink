import os
import json
import time
from minio import Minio
from minio.notificationconfig import NotificationConfig, QueueConfig
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MinIO connection settings
minio_server_url = os.environ.get('MINIO_SERVER_URL', 'http://minio-server:9000')
if minio_server_url.startswith('http://'):
    minio_server_url = minio_server_url[7:]  # Remove http:// prefix
elif minio_server_url.startswith('https://'):
    minio_server_url = minio_server_url[8:]  # Remove https:// prefix

minio_root_user = os.getenv('MINIO_ROOT_USER', 'admin')
minio_root_password = os.getenv('MINIO_ROOT_PASSWORD', 'admin@123')
bucket_name = os.getenv('BUCKET_NAME', 'mybucket')

# Kafka connection settings
kafka_bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
kafka_topic = os.getenv('KAFKA_TOPIC', 'minio-events')

def setup_minio_notifications(max_retries=3, retry_delay=5):
    """Set up MinIO bucket notifications to send events to Kafka"""
    for attempt in range(max_retries):
        try:
            # Initialize MinIO client
            client = Minio(
                minio_server_url,
                access_key=minio_root_user,
                secret_key=minio_root_password,
                secure=False
            )
            
            # Make sure bucket exists
            if not client.bucket_exists(bucket_name):
                client.make_bucket(bucket_name)
                print(f"Bucket '{bucket_name}' created successfully")
            
            # Create a notification configuration
            config = NotificationConfig()
            queue_config = QueueConfig(kafka_topic)
            queue_config.add_event_type("s3:ObjectCreated:*")
            queue_config.add_event_type("s3:ObjectRemoved:*")
            queue_config.add_event_type("s3:ObjectAccessed:*")
            config.add_queue_config(queue_config)
            
            # Set the notification configuration on the bucket
            client.set_bucket_notification(bucket_name, config)
            
            # Verify configuration
            current_config = client.get_bucket_notification(bucket_name)
            if current_config.queue_config_list:
                print("Notification configuration verified successfully")
                return True
            else:
                raise Exception("Notification configuration verification failed")
            
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed: {e}")
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"Final attempt failed: {e}")
                raise

if __name__ == "__main__":
    setup_minio_notifications()
    print("MinIO notification setup complete. Events will be sent to Kafka.")