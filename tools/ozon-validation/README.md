# OZON auto validation script 

## validation-service.sh 
This Bash script automates uploading a DSO publication .zip file, calculates its checksum and size, and performs validation against different DSO validation services.

## Prerequisites
- Bash environment
- Commands: `curl`, `scp`, `stat`, `jq` (optional for JSON)
- DSO API KEY

## Installation
1. Make the script executable if not already:

`chmod +x validation-service.sh`

2. Create a `.env` file and set DSO API KEY + file server config

`cp .env.example .env`

## Usage

`./validation-service.sh [-s service] <filename.zip>`

- `-s service`: (Optional) Service type (`partial`, `geo`, `full`). Default: `partial`.
- `<filename.zip>`: File to be processed.

## Features
- Dependency checks
- Multiple service endpoint support
- File size and checksum calculation
- File upload and validation

## Examples
Default service is partial:

`./validation-service.sh myfile.zip`

Specifying a service:

`./validation-service.sh -s geo myfile.zip`

