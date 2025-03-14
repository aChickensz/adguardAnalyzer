#!/bin/bash

# Prompt user for AdGuard Home details
read -p "Enter AdGuard Home Server IP (e.g., 192.168.1.1): " ADGUARD_IP
read -p "Enter AdGuard Username: " ADGUARD_USER
read -s -p "Enter AdGuard Password: " ADGUARD_PASS
echo
read -p "Enter Log Size (default 1000): " LOG_SIZE

# Set default log size if not provided
LOG_SIZE=${LOG_SIZE:-1000}

# Encode credentials in Base64
AUTH_HEADER=$(echo -n "$ADGUARD_USER:$ADGUARD_PASS" | base64)

# API Request to fetch logs and save to file
echo "Fetching the latest $LOG_SIZE logs from AdGuard Home..."
curl -s -H "Authorization: Basic $AUTH_HEADER" "http://$ADGUARD_IP/control/querylog?limit=$LOG_SIZE" -o adguard_queries.json

echo "Logs saved to adguard_queries.json"
