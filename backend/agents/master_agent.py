from backend.agents.email_agent import (
    get_recent_emails,
    search_email,
    read_email,
    summarize_email,
    send_new_email
)

from backend.agents.calendar_agent import (
    get_upcoming_events,
    search_calendar_events,
    schedule_event,
    update_calendar_event,
    cancel_calendar_event
)

from backend.memory.context_manager import (
    set_last_email,
    get_last_email,
    set_last_event,
    get_last_event,
    set_last_action,
    set_pending_cancellation,
    get_pending_cancellation,
    clear_pending_cancellation
)


pending_send_email = None


def process_request(user_message):

    global pending_send_email

    message = user_message.lower().strip()

    try:

        # CONFIRM SEND EMAIL

        if pending_send_email is not None:

            if message in [
                "yes",
                "yes send",
                "confirm",
                "confirm send"
            ]:

                data = pending_send_email

                result = send_new_email(
                    to=data["to"],
                    subject=data["subject"],
                    body=data["body"]
                )

                pending_send_email = None
                set_last_action("send_email")

                return {
                    "agent": "email",
                    "action": "send_email",
                    "result": result
                }

            if message in [
                "no",
                "no send",
                "don't send",
                "do not send",
                "cancel"
            ]:

                pending_send_email = None
                set_last_action("send_cancelled")

                return {
                    "agent": "email",
                    "action": "send_cancelled",
                    "message": "Email sending cancelled."
                }


        # CONFIRM CANCELLATION

        pending = get_pending_cancellation()

        if pending is not None:

            if message in [
                "yes",
                "yes cancel",
                "confirm",
                "confirm cancel"
            ]:

                result = cancel_calendar_event(
                    pending["event_id"]
                )

                clear_pending_cancellation()

                set_last_action(
                    "cancel_calendar_event"
                )

                return {
                    "agent": "calendar",
                    "action": "cancel_calendar_event",
                    "result": result
                }

            if message in [
                "no",
                "no cancel",
                "don't cancel",
                "do not cancel"
            ]:

                clear_pending_cancellation()

                set_last_action(
                    "cancel_cancelled"
                )

                return {
                    "agent": "calendar",
                    "action": "cancel_cancelled",
                    "message": "Cancellation cancelled."
                }


        # REQUEST SEND EMAIL

        if message.startswith("send email") and "|" in user_message:

            parts = user_message.split("|")

            if len(parts) != 4:

                return {
                    "agent": "email",
                    "success": False,
                    "error": "Invalid format. Use: Send email | TO | SUBJECT | BODY"
                }

            to = parts[1].strip()
            subject = parts[2].strip()
            body = parts[3].strip()

            pending_send_email = {
                "to": to,
                "subject": subject,
                "body": body
            }

            return {
                "agent": "email",
                "action": "confirm_send_email",
                "message": f"Are you sure you want to send this email to {to}?"
            }


        # REQUEST CANCELLATION

        if (
            "cancel it" in message
            or "cancel the meeting" in message
            or "cancel the event" in message
            or message == "cancel"
        ):

            event = get_last_event()

            if not event:

                return {
                    "agent": "calendar",
                    "success": False,
                    "error": "I do not have a previous calendar event in the conversation context."
                }

            event_id = event.get("id")

            if not event_id:

                return {
                    "agent": "calendar",
                    "success": False,
                    "error": "The previous event does not have a valid event ID."
                }

            set_pending_cancellation({
                "event_id": event_id,
                "summary": event.get(
                    "summary",
                    "this event"
                )
            })

            return {
                "agent": "calendar",
                "action": "confirm_cancellation",
                "message": f"Are you sure you want to cancel '{event.get('summary', 'this event')}'?"
            }


        # RESCHEDULE / UPDATE EVENT

        if (
            message.startswith("reschedule it")
            or message.startswith("reschedule event")
            or message.startswith("update event")
        ) and "|" in user_message:

            parts = user_message.split("|")

            if len(parts) != 3:

                return {
                    "agent": "calendar",
                    "success": False,
                    "error": "Invalid reschedule format. Use: Reschedule it | START ISO Time | END ISO Time"
                }

            event = get_last_event()

            if not event:

                return {
                    "agent": "calendar",
                    "success": False,
                    "error": "I do not have a previous calendar event in the conversation context."
                }

            event_id = event.get("id")

            if not event_id:

                return {
                    "agent": "calendar",
                    "success": False,
                    "error": "The previous event does not have a valid event ID."
                }

            start_time = parts[1].strip()
            end_time = parts[2].strip()

            result = update_calendar_event(
                event_id=event_id,
                start_time=start_time,
                end_time=end_time
            )

            if result.get("success"):

                set_last_event(
                    result.get("event")
                )

            set_last_action(
                "update_calendar_event"
            )

            return {
                "agent": "calendar",
                "action": "update_calendar_event",
                "result": result
            }


        # CREATE CALENDAR EVENT

        if message.startswith("schedule ") and "|" in user_message:

            parts = user_message.split("|")

            if len(parts) != 3:

                return {
                    "agent": "calendar",
                    "success": False,
                    "error": "Invalid schedule format."
                }

            summary = parts[0].replace(
                "schedule",
                "",
                1
            ).strip()

            start_time = parts[1].strip()
            end_time = parts[2].strip()

            result = schedule_event(
                summary=summary,
                start_time=start_time,
                end_time=end_time
            )

            if result.get("success"):

                set_last_event(
                    result.get("event")
                )

            set_last_action(
                "schedule_event"
            )

            return {
                "agent": "calendar",
                "action": "schedule_event",
                "result": result
            }


        # FOLLOW-UP: SUMMARIZE PREVIOUS EMAIL

        if (
            "summarize the first" in message
            or "summarize first" in message
            or "summarize it" in message
            or "summarize this" in message
        ):

            email = get_last_email()

            if not email:

                return {
                    "agent": "email",
                    "success": False,
                    "error": "I do not have a previous email in the conversation context."
                }

            result = summarize_email(
                email["id"]
            )

            set_last_action(
                "summarize_last_email"
            )

            return {
                "agent": "email",
                "action": "summarize_last_email",
                "result": result
            }


        # SEARCH EMAIL BY SENDER

        if (
            "email from" in message
            or "emails from" in message
        ):

            sender = user_message.lower().split(
                "from",
                1
            )[1].strip()

            emails = search_email(
                f"from:{sender}",
                10
            )

            if emails:

                set_last_email(
                    emails[0]
                )

            set_last_action(
                "search_email_by_sender"
            )

            return {
                "agent": "email",
                "action": "search_email_by_sender",
                "query": sender,
                "result": emails
            }


        # SEARCH EMAIL USING KEYWORDS

        if (
            ("find" in message or "search" in message)
            and
            ("email" in message or "emails" in message)
        ):

            keywords = (
                message
                .replace("find emails", "")
                .replace("find email", "")
                .replace("search emails", "")
                .replace("search email", "")
                .strip()
            )

            emails = search_email(
                keywords,
                10
            )

            if emails:

                set_last_email(
                    emails[0]
                )

            set_last_action(
                "search_email"
            )

            return {
                "agent": "email",
                "action": "search_email",
                "query": keywords,
                "result": emails
            }


        # LATEST EMAILS

        if (
            "latest email" in message
            or "latest emails" in message
            or "recent email" in message
            or "recent emails" in message
        ):

            emails = get_recent_emails(5)

            if emails:

                set_last_email(
                    emails[0]
                )

            set_last_action(
                "get_recent_emails"
            )

            return {
                "agent": "email",
                "action": "get_recent_emails",
                "result": emails
            }


        # SUMMARIZE EMAIL

        if (
            "summarize" in message
            and "email" in message
        ):

            emails = get_recent_emails(1)

            if not emails:

                return {
                    "agent": "email",
                    "success": False,
                    "error": "No emails found."
                }

            set_last_email(
                emails[0]
            )

            result = summarize_email(
                emails[0]["id"]
            )

            set_last_action(
                "summarize_email"
            )

            return {
                "agent": "email",
                "action": "summarize_email",
                "result": result
            }


        # CALENDAR EVENTS

        if (
            "calendar" in message
            or "event" in message
            or "meeting" in message
        ):

            if (
                "search" in message
                or "find" in message
            ):

                events = search_calendar_events(
                    message,
                    10
                )

                if events:

                    set_last_event(
                        events[0]
                    )

                set_last_action(
                    "search_calendar_events"
                )

                return {
                    "agent": "calendar",
                    "action": "search_events",
                    "result": events
                }

            events = get_upcoming_events(10)

            if events:

                set_last_event(
                    events[0]
                )

            set_last_action(
                "get_calendar_events"
            )

            return {
                "agent": "calendar",
                "action": "get_events",
                "result": events
            }


        return {
            "agent": "master",
            "success": False,
            "message": "I understood the request, but this action is not implemented yet.",
            "request": user_message
        }

    except Exception as error:

        return {
            "agent": "master",
            "success": False,
            "error": str(error)
        }