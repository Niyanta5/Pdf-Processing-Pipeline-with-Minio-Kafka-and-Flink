import os
from dotenv import load_dotenv

class Config:
    """Configuration manager for MinIO watcher and Kafka integration."""
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # MinIO configuration
        self.minio_server_url = os.environ.get('MINIO_SERVER_URL', '').replace('http://', '').replace('https://', '')
        self.minio_root_user = os.getenv('MINIO_ROOT_USER')
        self.minio_root_password = os.getenv('MINIO_ROOT_PASSWORD')
        self.bucket_name = os.getenv('MINIO_BUCKET_NAME', 'mybucket')
        self.minio_secure = os.getenv('MINIO_SECURE', 'false').lower() == 'true'
        
        # Kafka configuration
        self.kafka_bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.kafka_topic = os.getenv('KAFKA_TOPIC', 'minio-events')
        
        # Watcher configuration
        self.watch_directory = os.getenv('WATCH_DIRECTORY', './data')
        
        # Validate configuration
        self.validate()
        
    def validate(self):
        """Validate required configuration values."""
        if not all([self.minio_server_url, self.minio_root_user, self.minio_root_password]):
            raise ValueError("Missing required MinIO environment variables.")
    
    def print_config(self):
        """Print current configuration (excluding sensitive values)."""
        print(f"MINIO_SERVER_URL: {self.minio_server_url}")
        print(f"MINIO_ROOT_USER: {self.minio_root_user}")
        print(f"MINIO_ROOT_PASSWORD: {'*' * 8}")  # Don't print actual password
        print(f"MINIO_BUCKET_NAME: {self.bucket_name}")
        print(f"MINIO_SECURE: {self.minio_secure}")
        print(f"KAFKA_BOOTSTRAP_SERVERS: {self.kafka_bootstrap_servers}")
        print(f"KAFKA_TOPIC: {self.kafka_topic}")
        print(f"WATCH_DIRECTORY: {self.watch_directory}")