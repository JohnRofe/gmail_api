'''Module to parse and decode the message from the Gmail API.'''

import re
import base64

def catch_body(message):
    '''
    Extracts the 'data' field from the message body.

    Returns:
    str: The 'data' field from the message body if found, else None.
    '''
    match = re.search(r"'data': '(.*?)'", message) #This searches for the body of the message
    return match.group(1) if match else None

def decoder(message):
    '''
    Decodes the 'data' field from the message body.

    Returns:
    bytes: The decoded 'data' field from the message body if found, else None.
    '''
    body = catch_body(message)
    return base64.urlsafe_b64decode(body) if body else None

def main(message):
    '''
    Main function to decode the message.

    Returns:
    bytes: The decoded message.
    '''
    return decoder(message)

if __name__ == '__main__':
    # The raw message is stored in 'example.txt'
    with open('example.txt', 'r') as file:
        message = file.read()
    print(main(message))