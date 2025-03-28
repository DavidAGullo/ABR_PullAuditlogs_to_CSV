import os
import sys
import csv
import json
import requests
import logging
from dotenv import load_dotenv
from datetime import datetime

# IMPORTANT VARIABLES
datacenter = "dc2"  # Data center to connect to (DC1 = EU, DC2 = US, etc.)
api = "auditlog"
days = 365  # Number of days to retrieve logs for
entries = 10000  # Number of entries to retrieve

url = f"https://dc2api.adminbyrequest.com/{api}?days={days}&take={entries}"
apikey = os.getenv("API_KEY")  # API key for authentication


#!/usr/bin/env python3
"""
auditlog.py

Author: David Gullo
Date: 2024-03-27
Version: 1.0
Description:
This script connects to an API endpoint to retrieve audit logs and saves them in a CSV format.

Usage:
    python auditlog.py
Dependencies:
    - requests
    - csv
    - logging
    - datetime
    - os
    - sys  
    - json
    - dotenv - optional
"""


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def main():
    logging.info("Starting the audit log processing script...")
    # Making the Request to the API
    
    # Check if API_KEY is set
    if not apikey:
        logging.error("API_KEY environment variable not set.")
        sys.exit(1)
        
    headers = {
        "apikey": apikey,
        "Content-Type": "application/csv"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        logging.info("Successfully retrieved audit logs.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching audit logs: {e}")
        sys.exit(1)
    # Process the response
    data = response.json()
    if not data:
        logging.info("No audit logs found.")
        return
    # Save the response to a file
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"elevated_apps.json"
    # Open the Json response
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    logging.info(f"Audit logs saved to {filename}.")
    # Convert JSON to CSV
        
    rows = []
    # Open the CSV file for writing
    for record in data:
        # Flattening common fields
        base = {
            'id': record.get('id'),
            'traceNo': record.get('traceNo'),
            'user_account': record.get('user', {}).get('account'),
            'computer_name': record.get('computer', {}).get('name'),
            'platform': record.get('computer', {}).get('platform'),
            'status': record.get('status'),
            'application_name': record.get('application', {}).get('name'),
            'requestTime': record.get('requestTime')
        }
        # If there are elevated applications, write one row per
        for app in record.get('elevatedApplications', []):
            row = base.copy()
            row.update({
                'app_name': app.get('name'),
                'app_path': app.get('path'),
                'app_file': app.get('file'),
                'app_version': app.get('version'),
                'vendor': app.get('vendor'),
                'scanResult': app.get('scanResult'),
                'virustotalLink': app.get('virustotalLink'),
            })
            rows.append(row)
    try:
        with open('elevated_apps.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = rows[0].keys() if rows else []
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
    except PermissionError as e:
        logging.error(f"Permission denied: {e}")
    except IsADirectoryError as e:
        logging.error(f"Expected a file but found a directory: {e}")
    except OSError as e:
        logging.error(f"OS error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    logging.info("Audit log processing script completed.")


if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file if present
    main()
