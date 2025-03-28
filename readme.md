# Audit Log Exporter

This script retrieves audit logs from the Admin By Request API and exports them into both JSON and CSV formats. It is designed to simplify the process of pulling detailed elevation request logs and their associated application data.

## Features

- Connects to the Admin By Request API
- Retrieves audit logs for a configurable number of days and entries
- Saves the raw data to a .json file
- Extracts and flattens key data into a .csv file for easy analysis
- Logs progress and errors to the console
- Supports .env files for API key management

## Requirements

- Python 3.6+
- Python Packages:
    - requests
    - python-dotenv (load_dotenv)

### Install Dependency

```bash
pip install -r requirements.txt
```
if requirements.txt does not exist, create it with:
```txt
requests
python-dotenv
```

## Setup

1. Clone or Download the script to your local machine
2. Set up your environment variables:
    - Create a .env file in the same directory as the script.
    - Add your API key:
    ```env
    API_KEY=your_admin_by_request_api_key
    ```
3. (Optional) Modify the script to change:
    - datacenter (e.g., "dc1" for EU or "dc2" for US)
    - Number of days or entries to retrieve
    - api endpoint if needed

## Usage

Run:
```bash
python auditlog.py
```
Upon execution:
- A elevated_apps.json file is created containing the full API response.
- A elevated_apps.csv file is generated with flattened and filtered fields for analysis.

## Output Fields (CSV)

Each row represents an elevated application entry and includes:
- id
- traceNo
- user_account
- computer_name
- platform
- status
- application_name
- requestTime
- app_name
- app_path
- app_file
- app_version
- vendor
- scanResult
- virustotalLink

## Logging

The script outputs progress and errors to the console using Python's logging module.

## Troubleshooting

- Make sure your .env file exists and contains a valid API_KEY.
- Ensure your firewall or proxy does not block requests to the Admin By Request API.
- Run with sufficient permissions to write output files in the script directory.

