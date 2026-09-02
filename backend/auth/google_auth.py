import os
import json
import base64
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


BASE_DIR = Path(__file__).resolve().parents[2]

CREDENTIALS_FILE = BASE_DIR / "backend" / "auth" / "credentials.json"
TOKEN_FILE = BASE_DIR / "backend" / "auth" / "token.json"

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar",
]


def get_google_credentials():
    creds = None

    token_b64 = os.getenv("GOOGLE_TOKEN_B64")
    credentials_b64 = os.getenv("GOOGLE_CREDENTIALS_B64")

    if token_b64:
        try:
            token_info = json.loads(
                base64.b64decode(token_b64).decode("utf-8")
            )

            if credentials_b64:
                credentials_info = json.loads(
                    base64.b64decode(credentials_b64).decode("utf-8")
                )

                client_info = (
                    credentials_info.get("installed")
                    or credentials_info.get("web")
                )

                token_info.setdefault(
                    "client_id",
                    client_info.get("client_id")
                )
                token_info.setdefault(
                    "client_secret",
                    client_info.get("client_secret")
                )
                token_info.setdefault(
                    "token_uri",
                    client_info.get("token_uri")
                )

            creds = Credentials.from_authorized_user_info(
                token_info,
                SCOPES
            )

        except Exception:
            creds = None

    if creds is None and TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(
                str(TOKEN_FILE),
                SCOPES
            )
        except Exception:
            creds = None

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())

            if not token_b64:
                TOKEN_FILE.write_text(creds.to_json())

            return creds

        except Exception:
            creds = None

    if not CREDENTIALS_FILE.exists():
        raise FileNotFoundError(
            f"Google credentials file not found: {CREDENTIALS_FILE}"
        )

    flow = InstalledAppFlow.from_client_secrets_file(
        str(CREDENTIALS_FILE),
        SCOPES
    )

    creds = flow.run_local_server(
        port=0,
        access_type="offline",
        prompt="consent"
    )

    TOKEN_FILE.write_text(creds.to_json())

    return creds