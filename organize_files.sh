#!/bin/bash

# Ensure we are in the project root directory
# Adjust path if needed
cd "$(dirname "$0")"

echo "Starting organization..."

# 1. Move Archive Files
# Assuming 'archive', 'logs', 'notes', and 'deprecated_scripts' exist
mkdir -p archive/logs archive/notes archive/deprecated_scripts

# Move old logs and scripts (adjust pattern based on your filenames)
mv *.csv archive/logs/ 2>/dev/null
mv *.py archive/deprecated_scripts/ 2>/dev/null
# Note: Be careful moving EVERYTHING to archive, 
# you might want to move specific files instead.

# 2. Move Webhook Files
mkdir -p trakker-ingest-webhook
mv server.js package.json trakker-ingest-webhook/ 2>/dev/null

# 3. Move Analytics Files
mkdir -p trakker-analytics-api
mv clean_logs_v3.py auth.py server.py trakker-analytics-api/ 2>/dev/null

# 4. Move Data Files
mkdir -p data
mv raw_logs.csv tiguan_logs.csv data/ 2>/dev/null

echo "Organization complete!"