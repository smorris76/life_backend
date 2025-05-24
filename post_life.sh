#!/bin/bash

# Usage: ./post_life.sh path/to/life.json

if [ -z "$1" ]; then
  echo "Usage: $0 path/to/json_file"
  exit 1
fi

JSON_FILE="$1"

# Ensure API token is set
if [ -z "$API_TOKEN" ]; then
  echo "Error: API_TOKEN environment variable not set"
  exit 1
fi

# Read and send the file
curl -X POST http://localhost:8443/life \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  --data-binary "@$JSON_FILE"
