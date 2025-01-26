#!/bin/bash

# Script to generate and upload a video to YouTube Shorts

# Determine which Python interpreter to use
if command -v python3 &> /dev/null; then
  PYTHON=python3
elif command -v python &> /dev/null; then
  PYTHON=python
else
  echo "Python is not installed. Please install Python to proceed."
  exit 1
fi

# Define the YouTube cache file path
YOUTUBE_CACHE=".mp/youtube.json"

# Check if the YouTube cache file exists
if [ ! -f "$YOUTUBE_CACHE" ]; then
  echo "YouTube cache file not found at $YOUTUBE_CACHE."
  echo "Ensure the file exists and contains account information."
  exit 1
fi

# Read account IDs from the YouTube cache file
youtube_ids=$($PYTHON -c "import json; print('\n'.join([account['id'] for account in json.load(open('$YOUTUBE_CACHE'))['accounts']]))")

# If no account IDs are found, exit
if [ -z "$youtube_ids" ]; then
  echo "No YouTube accounts found in $YOUTUBE_CACHE."
  exit 1
fi

# Prompt user to select an account
echo "Available YouTube account IDs:"
echo "$youtube_ids"

read -p "Enter the ID of the account you want to upload the video to: " id

# Validate the entered ID
if echo "$youtube_ids" | grep -q "^$id$"; then
  echo "ID found: $id"
else
  echo "ID not found. Please ensure you enter a valid ID from the list above."
  exit 1
fi

# Run the Python script with the selected account ID
$PYTHON src/cron.py youtube "$id"
if [ $? -eq 0 ]; then
  echo "Video uploaded successfully."
else
  echo "An error occurred during video upload. Check the logs for more details."
fi
