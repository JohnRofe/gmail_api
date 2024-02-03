'''
This script reads emails from a bank and creates a dataframe for personal finance.
'''

# Importing required libraries
import os
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Personal libraries
import decoder
import html_parser

def get_token(path, scopes):
    '''
    Returns token for Google APIs and Services.

    Parameters:
    path (str): Path of credentials.json file downloaded from Google Cloud Console.
    scopes (list): Scopes of your service.

    Returns:
    token: Google API token.

    Requirements 
    credentials.json 

    '''
    PATH = path
    SCOPES = scopes
    token = None

    # Checks for existing tokens.
    if os.path.exists('token_creds.json'):
        token = Credentials.from_authorized_user_file('token_creds.json', SCOPES)

    # If there are no (valid) tokens available, let it retrieve new tokens.
    if not token or not token.valid:
        if token and token.expired and token.refresh_token:
            token.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(PATH, SCOPES)
            token = flow.run_local_server(port=0)

        # Saves the credentials for later use.
        with open('token_creds.json', 'w') as f:
            f.write(token.to_json())

    return token

def create_service():
    '''
    Creates a service object for the Gmail API.

    Returns:
    service: Gmail API service object.
    '''
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = get_token('credentials.json', SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    return service

def get_messages(service, user_id, maxResults=500, pageToken=None):
    '''
    Retrieves messages.

    Parameters:
    service: Gmail API service object.
    user_id (str): User ID.
    maxResults (int, optional): Maximum results. Defaults to 500, instead of 100.
    pageToken (str, optional): Page token. Defaults to None.

    Returns:
    dict: Messages.
    '''
    try:
        if pageToken:
            return service.users().messages().list(userId=user_id, labelIds=['YOUR LABEL'], maxResults=maxResults, pageToken=pageToken).execute()
        else:
            return service.users().messages().list(userId=user_id, labelIds=['YOUR LABEL'], maxResults=maxResults).execute()
    except Exception as error:
        print('An error occurred: %s' % error)

def main():
    '''
    Main function to process messages and create a DataFrame.
    '''
    get_token('credentials.json', ['https://www.googleapis.com/auth/gmail.readonly'])
    service = create_service()

    # Check if BAC.csv exists
    if os.path.exists('BAC.csv'): # raw csv 
        mode = 'a' # append if already exists
    else:
        mode = 'w' # write if does not exist

    # Get list of messages 
    messages_result = get_messages(service, 'me')
    messages = messages_result.get('messages', [])

    if not messages:
        print("No messages found.")
    else:
        # Initialize an empty list
        data_list = []
        last_processed_msg_id = None

        # Process each message
        for i, msg in enumerate(messages):
            msg_id = msg['id']

            # Fetch full message
            try:
                message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
            except HttpError as error:
                if error.resp.status == 429:
                    print("Rate limit exceeded. Last processed message ID: ", last_processed_msg_id)
                    break
                else:
                    raise

            # Turn the message into a string
            message = str(message)

            # Use the decoder to decode the message
            decoded_message = decoder.main(message)

            # Use the parser to parse the html
            parsed_html = html_parser.parse_html(decoded_message)
        
            # Append the parsed data to the list
            data_list.append(parsed_html)

            # Save the last processed message ID
            last_processed_msg_id = msg_id

            # Print progress every 15 emails
            if (i + 1) % 15 == 0:
                print(f"Processed {i + 1} emails so far.")
        
        # Convert the list to a DataFrame
        df = pd.DataFrame(data_list, columns=['YOUR COLUMNS'])

        # Create a CSV file from the DataFrame
        df.to_csv('DATA.csv', mode=mode, header=not os.path.exists('DATA.csv'), index=False)
                    
if __name__ == '__main__':
    main()
                    







