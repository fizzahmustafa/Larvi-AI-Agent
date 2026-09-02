from backend.services.gmail_service import get_latest_emails, get_email_content


emails = get_latest_emails(1)

if not emails:
    print("No emails found.")
else:
    latest_email = get_email_content(emails[0]["id"])

    print("\n===== LATEST EMAIL =====")
    print("From:", latest_email["from"])
    print("Subject:", latest_email["subject"])
    print("Date:", latest_email["date"])
    print("\n===== EMAIL CONTENT =====")
    print(latest_email["body"])