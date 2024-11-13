import os
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.apps import chat_v1 as google_chat
from flask import Flask, request, jsonify

load_dotenv()

app = Flask(__name__)

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# declaring SCOPES
SCOPES = ['https://www.googleapis.com/auth/chat.spaces.readonly',
          'https://www.googleapis.com/auth/spreadsheets.readonly',
          'https://www.googleapis.com/auth/drive.appdata']


# ... code for Google API authentication
# TODO: modular code

def main():
    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        client = google_chat.ChatServiceClient(
            credentials = creds,
            client_options = {
                "scopes" : SCOPES
            }
        )

        request = google_chat.ListSpacesRequest(
            filter = 'space_type = "SPACE"'
        )

        page_result = client.list_spaces(request)

        for response in page_result:
            print(response)

    except Exception as error:
        # TODO
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
