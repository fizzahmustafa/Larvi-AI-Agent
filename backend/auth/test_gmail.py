from .gmail_auth import get_gmail_service


def test_gmail():
    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me",
        maxResults=5
    ).execute()

    messages = results.get("messages", [])

    print("\nGMAIL CONNECTION SUCCESSFUL!\n")

    if not messages:
        print("No messages found.")
        return

    print(f"Found {len(messages)} emails:\n")

    for i, message in enumerate(messages, start=1):
        email = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="metadata",
            metadataHeaders=["From", "Subject"]
        ).execute()

        headers = email.get("payload", {}).get("headers", [])

        header_data = {
            header["name"]: header["value"]
            for header in headers
        }

        print(f"{i}. From: {header_data.get('From', 'Unknown')}")
        print(f"   Subject: {header_data.get('Subject', 'No Subject')}")
        print()


if __name__ == "__main__":
    test_gmail()
