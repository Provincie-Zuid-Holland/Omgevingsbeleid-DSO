#!/bin/bash
. ./.env

# --service partion/full/geo
service="partial"

# Parse command-line arguments
while getopts ":s:" opt; do
  case $opt in
    s) service="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
       exit 1
    ;;
  esac
done

# Shift off the options and optional --
shift $((OPTIND-1))

# Conditional logic based on --service argument
if [ "$service" = "partial" ]; then
    echo "Selected service: Partial"
    SERVICE_URL=$VALIDATION_SERVICE_OW_PARTIAL
    REPORT_URL=$VALIDATION_SERVICE_OW_REPORT
elif [ "$service" = "geo" ]; then
    echo "Selected service: Geo"
    SERVICE_URL=$VALIDATION_SERVICE_GEO
    REPORT_URL=$VALIDATION_SERVICE_GEO_REPORT
elif [ "$service" = "full" ]; then
    echo "Selected service: Full"
    SERVICE_URL=$VALIDATION_SERVICE_OW_FULL
    REPORT_URL=$VALIDATION_SERVICE_OW_REPORT
else
    echo "Error: Invalid service specified."
    exit 1
fi

# Function to check if a command exists
command_exists() {
    if ! command -v $1 &> /dev/null; then
        echo "Error: Required command '$1' is not installed."
        exit 1
    fi
}

# Check for system dependencies
if [[ "$(uname)" == "Darwin" ]]; then
    # macOS system
    MD5_CMD="shasum -a 256"
    STAT_CMD="stat -f%z"
else
    # Linux or other system
    MD5_CMD="sha256sum"
    STAT_CMD="stat -c%s"
    command_exists "sha256sum"
fi

command_exists "curl"
command_exists "scp"
command_exists "stat"

# Function to handle HTTP request errors
handle_http_error() {
    if [ "$1" != "200" ]; then
        echo "HTTP request failed with status code $1"
        exit 2
    fi
}

# Check if an argument is provided and if the file exists
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <filename.zip>"
    exit 1
fi

filename=$1

if [ ! -f "$filename" ]; then
    echo "Error: File '$filename' not found."
    exit 1
fi

# Calculate file size in bytes and MD5 checksum
file_size=$($STAT_CMD "$filename")
md5_checksum=$($MD5_CMD "$filename" | awk '{ print $1 }')

# Print size and checksum
echo "File Size: $file_size"
echo "MD5 Checksum: $md5_checksum"

# Upload file to the server
RESPONSE=$(curl -u $FILE_SERVER_USER:$FILE_SERVER_PASS -X POST -F "file=@$filename" $FILE_SERVER_ENDPOINT -w "\nHTTP Status Code: %{http_code}\n")
echo "Server Response:"
echo "$RESPONSE"


# VALIDATE
validation_url="$FILE_SERVER/$filename"
if [ "$service" = "partial" ] || [ "$service" = "full" ]; then
    post_data='{
        "identificatie": "'"$filename"'",
        "checksum": "'"$md5_checksum"'",
        "grootte": '"$file_size"',
        "url": "'"$validation_url"'",
        "typeOmgevingsdocument": "ONTWERPREGELING"
    }'
else
    post_data='{
        "identificatie": "'"$filename"'",
        "checksum": "'"$md5_checksum"'",
        "grootte": '"$file_size"',
        "url": "'"$validation_url"'"
    }'
fi
echo "Sending POST request with the following data:"
echo "$post_data"

post_response=$(curl -s -o /tmp/response_body.txt -w "%{http_code}" -X POST "$SERVICE_URL" \
-H "Content-Type: application/json" \
-H "X-Api-Key: $DSO_API_KEY" \
-d "$post_data")

handle_http_error "$post_response"
uuid=$(< /tmp/response_body.txt)
echo "UUID: $uuid"

# REPORT
report_url="$REPORT_URL/$uuid" 
json_response=$(curl -s -X GET $report_url \
-H "X-Api-Key: $DSO_API_KEY")

if command -v jq &> /dev/null; then
    echo "pretty-printed json response:"
    echo "$json_response" | jq .
else
    echo "json response (raw):"
    echo "$json_response"
fi


# Clean up 
rm /tmp/response_body.txt
