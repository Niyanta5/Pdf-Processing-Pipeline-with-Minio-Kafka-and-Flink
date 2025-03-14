
# PDF Pipeline

A distributed pipeline for generating and processing PDFs using Apache Flink and Apache Kafka.

## Architecture

```
[PDF Generator] -> [MinIO + Kafka] -> [Flink Processing] -> [Output Storage]
```

The pipeline consists of:
- PDF Generator service for creating PDFs
- MinIO for object storage
- Kafka for event streaming
- Flink for distributed processing

## Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Java 11+ (for Apache Flink)

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd pdf-pipeline
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download Flink connectors:
```bash
./scripts/download_dependencies.sh
```

5. Start the infrastructure:
```bash
docker-compose up -d
```

6. Wait for all services to be healthy (approximately 1-2 minutes)

## Usage

### Generate and Upload PDFs

```python
from src.pdf_generator import PDFGenerator
from src.minio_handler import MinioHandler

generator = PDFGenerator()
handler = MinioHandler()

# Generate and upload a PDF
pdf_data = generator.generate_pdf()
object_name = handler.upload_pdf(pdf_data, metadata={"source": "test"})
```

### Start the Flink Consumer

```bash
python src/flink_consumer.py
```

## Service URLs

- MinIO Console: http://localhost:9001 (login: minioadmin/minioadmin)
- Flink Dashboard: http://localhost:8081
- Kafka: localhost:9092
- MinIO API: localhost:9000

## Project Structure

```
pdf-pipeline/
├── src/
│   ├── config.py           # Configuration settings
│   ├── pdf_generator.py    # PDF generation logic
│   ├── minio_handler.py    # MinIO and Kafka integration
│   └── flink_consumer.py   # Flink processing job
├── scripts/
│   └── download_dependencies.sh  # Downloads required JARs
├── docker-compose.yml      # Infrastructure setup
└── requirements.txt        # Python dependencies
```

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black src/
```

## Troubleshooting

1. If Flink jobs fail to start, ensure:
   - All required JARs are in the `lib/` directory
   - Kafka and MinIO services are running
   - Correct versions of connectors are being used

2. If PDFs fail to upload:
   - Check MinIO credentials
   - Verify MinIO bucket exists
   - Ensure proper network connectivity

## Dependencies

- Apache Flink 1.18.1
- Apache Kafka
- MinIO
- Python Libraries (see requirements.txt)


## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
