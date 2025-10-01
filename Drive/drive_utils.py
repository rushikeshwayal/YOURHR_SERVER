import os, io
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.credentials import Credentials

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/drive.file",
]

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")


def get_authorization_url():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI],
            }
        },
        scopes=SCOPES,
    )
    flow.redirect_uri = REDIRECT_URI
    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )
    return auth_url, state


def exchange_code_for_credentials(code: str) -> Credentials:
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI],
            }
        },
        scopes=SCOPES,
    )
    flow.redirect_uri = REDIRECT_URI
    flow.fetch_token(code=code)
    return flow.credentials


def upload_file_to_drive(file_name: str, file_content: io.BytesIO, mime_type: str, credentials: Credentials):
    drive_service = build("drive", "v3", credentials=credentials)
    file_metadata = {"name": file_name}
    if FOLDER_ID:
        file_metadata["parents"] = [FOLDER_ID]

    media = MediaIoBaseUpload(file_content, mimetype=mime_type, resumable=True)
    uploaded_file = drive_service.files().create(
        body=file_metadata, media_body=media, fields="id"
    ).execute()
    return f"https://drive.google.com/uc?id={uploaded_file.get('id')}"
