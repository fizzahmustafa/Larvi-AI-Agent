from backend.services.gmail_service import (
    get_latest_emails,
    search_emails,
    get_email_content,
    create_email_draft,
    send_email
)

from backend.services.llm_service import generate_response


def get_recent_emails(max_results=5):
    return get_latest_emails(max_results)


def search_email(query, max_results=5):
    return search_emails(query, max_results)


def read_email(message_id):
    return get_email_content(message_id)


def summarize_email(message_id):
    email = get_email_content(message_id)

    prompt = f"""
Summarize the following email clearly and briefly.

From: {email["from"]}
Subject: {email["subject"]}
Date: {email["date"]}

Email:
{email["body"]}
"""

    summary = generate_response(prompt)

    return {
        "id": email["id"],
        "from": email["from"],
        "subject": email["subject"],
        "date": email["date"],
        "summary": summary
    }


def draft_email(to, subject, body):
    return create_email_draft(
        to=to,
        subject=subject,
        body=body
    )


def send_new_email(to, subject, body):
    return send_email(
        to=to,
        subject=subject,
        body=body
    )
