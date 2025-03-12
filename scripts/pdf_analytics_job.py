from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.connectors import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.common.typeinfo import Types
import json
import os

def main():
    # Create streaming environment
    env = StreamExecutionEnvironment.get_execution_environment()
    
    # Add Kafka connector dependencies
    kafka_jar = "flink-sql-connector-kafka_2.12-1.18.0.jar"
    env.add_jars(f"file:///opt/flink/lib/{kafka_jar}")

    # Kafka consumer properties
    props = {
        'bootstrap.servers': 'kafka:9092',
        'group.id': 'pdf-analytics-group'
    }

    # Create Kafka source
    kafka_consumer = FlinkKafkaConsumer(
        topics='minio-events',
        deserialization_schema=SimpleStringSchema(),
        properties=props
    )

    # Create Kafka sink for processed events
    kafka_producer = FlinkKafkaProducer(
        topic='pdf-analytics',
        serialization_schema=SimpleStringSchema(),
        producer_config=props
    )

    def process_pdf_event(event):
        """Process PDF events and extract analytics"""
        try:
            data = json.loads(event)
            if 'Records' in data:
                record = data['Records'][0]
                
                # Extract relevant information
                event_time = record['eventTime']
                event_name = record['eventName']
                object_key = record['s3']['object']['key']
                size = record['s3']['object']['size']
                
                # Create analytics record
                analytics = {
                    'timestamp': event_time,
                    'event_type': event_name,
                    'file_name': object_key,
                    'file_size': size,
                    'file_type': 'pdf' if object_key.endswith('.pdf') else 'other',
                    'processing_time': time.time()
                }
                
                return json.dumps(analytics)
        except Exception as e:
            return json.dumps({'error': str(e), 'original_event': event})

    # Create processing pipeline
    (
        env.add_source(kafka_consumer)
        .map(process_pdf_event)
        .filter(lambda x: x is not None)
        .add_sink(kafka_producer)
    )

    # Execute the job
    env.execute("PDF Analytics Job")

if __name__ == '__main__':
    main()