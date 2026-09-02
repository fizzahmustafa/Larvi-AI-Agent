import base64

from backend.auth.gmail_auth import get_gmail_service


def get_latest_emails(max_results=5):
    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me",
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])

    emails = []

    for message in messages:
        email = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="metadata",
            metadataHeaders=["From", "Subject", "Date"]
        ).execute()

        headers = email.get("payload", {}).get("headers", [])

        header_data = {
            header["name"]: header["value"]
            for header in headers
        }

        emails.append({
            "id": message["id"],
            "from": header_data.get("From", "Unknown"),
            "subject": header_data.get("Subject", "No Subject"),
            "date": header_data.get("Date", "Unknown")
        })

    return emails


def search_emails(query, max_results=5):
    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])

    return messages


def get_email_content(message_id):
    service = get_gmail_service()

    email = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

    payload = email.get("payload", {})

    headers = payload.get("headers", [])

    header_data = {
        header["name"]: header["value"]
        for header in headers
    }

    body = ""

    if "data" in payload.get("body", {}):
        body = base64.urlsafe_b64decode(
            payload["body"]["data"]
        ).decode("utf-8", errors="ignore")

    elif "parts" in payload:
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data")

                if data:
                    body = base64.urlsafe_b64decode(
                        data
                    ).decode("utf-8", errors="ignore")
                    break

    return {
        "id": message_id,
        "from": header_data.get("From", "Unknown"),
        "subject": header_data.get("Subject", "No Subject"),
        "date": header_data.get("Date", "Unknown"),
        "body": body
    }


def print_latest_emails(max_results=5):
    emails = get_latest_emails(max_results)

    if not emails:
        print("No emails found.")
        return

    print(f"\nLatest {len(emails)} emails:\n")

    for i, email in enumerate(emails, start=1):
        print(f"{i}. From: {email['from']}")
        print(f"   Subject: {email['subject']}")
        print(f"   Date: {email['date']}")
        print()


if __name__ == "__main__":
    print_latest_emails()
def create_email_draft(to, subject, body):
    from email.mime.text import MIMEText

    service = get_gmail_service()

    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject

    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode("utf-8")

    draft = service.users().drafts().create(
        userId="me",
        body={
            "message": {
                "raw": raw_message
            }
        }
    ).execute()

    return {
        "success": True,
        "draft_id": draft.get("id"),
        "message": "Email draft created successfully"
    }


def send_email(to, subject, body):
    from email.mime.text import MIMEText

    service = get_gmail_service()

    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject

    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode("utf-8")

    sent_message = service.users().messages().send(
        userId="me",
        body={
            "raw": raw_message
        }
    ).execute()

    return {
        "success": True,
        "message": "Email sent successfully",
        "message_id": sent_message.get("id")
    }
