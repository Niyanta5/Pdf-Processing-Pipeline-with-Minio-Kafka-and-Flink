import os
import json
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

def setup_minio_notifications():
    """Set up MinIO bucket notifications to send events to Kafka"""
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
        
        # Add a queue (Kafka) configuration
        queue_config = QueueConfig(kafka_topic)
        
        # Add events to the queue configuration
        queue_config.add_event_type("s3:ObjectCreated:*")
        queue_config.add_event_type("s3:ObjectRemoved:*")
        queue_config.add_event_type("s3:ObjectAccessed:*")
        
        # Add the queue configuration to the notification configuration
        config.add_queue_config(queue_config)
        
        # Set the notification configuration on the bucket
        client.set_bucket_notification(bucket_name, config)
        
        print(f"MinIO notification for bucket '{bucket_name}' configured successfully")
        
        # Verify configuration was set correctly
        current_config = client.get_bucket_notification(bucket_name)
        if current_config.queue_config_list:
            print("Notification configuration verified successfully")
        else:
            print("Warning: Notification configuration may not have been applied correctly")
        
    except Exception as e:
        print(f"Error setting up MinIO notifications: {e}")
        raise

if __name__ == "__main__":
    setup_minio_notifications()
    print("MinIO notification setup complete. Events will be sent to Kafka.")