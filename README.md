# Immich-Upload-Script

A simple Python script to automatically upload new or updated images from multiple folders on Windows to an Immich server via its API.

## Requirements

- Python 3.x
- `requests` library (`pip install requests`)

## Setup

1. Configure your Immich API key and server URL in the script.
2. Add the folders you want to monitor to the `UPLOAD_FOLDERS` list.
3. Run the script manually or add it to Windows startup for automatic execution on boot.
