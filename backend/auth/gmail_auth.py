from googleapiclient.discovery import build

from .google_auth import get_google_credentials


def get_gmail_service():

    credentials = get_google_credentials()

    return build(
        "gmail",
        "v1",
        credentials=credentials
    )


if __name__ == "__main__":
    print("Starting Google authentication...")

    service = get_gmail_service()

    print("Google authentication successful!")
    print("Gmail service is ready.")
