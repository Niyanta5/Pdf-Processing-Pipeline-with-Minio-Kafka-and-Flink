#!/bin/bash

# Function to upload a file to MinIO
upload_file() {
    local source_file=$1
    local filename=$(basename $source_file)
    echo "Uploading $filename to MinIO..."
    docker cp "$source_file" minio-server:/data/
    docker exec minio-server mc cp "/data/$filename" myminio/mybucket/
}

# Function to download a file from MinIO
download_file() {
    local filename=$1
    local dest_dir=${2:-"data/downloads"}
    mkdir -p "$dest_dir"
    echo "Downloading $filename from MinIO..."
    docker exec minio-server mc cp "myminio/mybucket/$filename" "/data/$filename"
    docker cp "minio-server:/data/$filename" "$dest_dir/"
}

# Function to list files in bucket
list_files() {
    echo "Listing files in MinIO bucket..."
    docker exec minio-server mc ls myminio/mybucket/
}

# Function to delete a file
delete_file() {
    local filename=$1
    echo "Deleting $filename from MinIO..."
    docker exec minio-server mc rm "myminio/mybucket/$filename"
}

# Create test files
mkdir -p data
echo "Creating test files..."
echo "PDF test content" > data/test.pdf
echo "Text test content" > data/test.txt

# Test operations
echo "Testing MinIO operations..."

echo "1. Uploading files..."
upload_file "data/test.pdf"
upload_file "data/test.txt"

echo "2. Listing files..."
list_files

echo "3. Downloading files..."
download_file "test.pdf"
download_file "test.txt"

echo "4. Deleting files..."
delete_file "test.pdf"
delete_file "test.txt"

echo "5. Final file listing..."
list_files

echo "Test complete!"