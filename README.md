# Gmail Message Parser

This project contains a collection of scripts for retrieving messages from Gmail and parsing specific data fields.

The `gmail.py` script fetches messages, the `decoder.py` module handles decoding the message payloads, and the `html_parser.py` module parses fields from HTML email contents.

These components combine to allow extracting custom fields from Gmail messages received in an HTML format, and outputting the parsed data to a CSV file.

## Usage

The `gmail.py` main script handles the overall workflow:

1. Authenticate with Gmail API
2. Fetch messages with label
3. Decode messages 
4. Parse HTML contents
5. Write parsed data to CSV

Modify `gmail.py` to provide necessary credentials and target label details.


