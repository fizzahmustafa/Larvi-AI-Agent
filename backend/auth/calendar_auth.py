from googleapiclient.discovery import build

from .google_auth import get_google_credentials


def get_calendar_service():
    """
    Return an authenticated Google Calendar API service.
    """
    credentials = get_google_credentials()

    return build(
        "calendar",
        "v3",
        credentials=credentials
    )
