from datetime import datetime, timezone

from backend.auth.calendar_auth import get_calendar_service


def format_event(event):
    start = event.get("start", {})
    end = event.get("end", {})

    return {
        "id": event.get("id"),
        "summary": event.get("summary", "No title"),
        "description": event.get("description", ""),
        "start": start.get("dateTime", start.get("date", "")),
        "end": end.get("dateTime", end.get("date", "")),
        "location": event.get("location", ""),
        "status": event.get("status", "")
    }


def get_events(max_results=10):
    service = get_calendar_service()

    now = datetime.now(timezone.utc).isoformat()

    result = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    return [format_event(event) for event in result.get("items", [])]


def search_events(query, max_results=10):
    service = get_calendar_service()

    result = service.events().list(
        calendarId="primary",
        q=query,
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    return [format_event(event) for event in result.get("items", [])]


def get_event(event_id):
    service = get_calendar_service()

    event = service.events().get(
        calendarId="primary",
        eventId=event_id
    ).execute()

    return format_event(event)


def check_availability(start_time, end_time):
    service = get_calendar_service()

    body = {
        "timeMin": start_time,
        "timeMax": end_time,
        "items": [
            {"id": "primary"}
        ]
    }

    result = service.freebusy().query(body=body).execute()

    busy = result["calendars"]["primary"].get("busy", [])

    return {
        "available": len(busy) == 0,
        "busy_periods": busy
    }


def create_event(summary, start_time, end_time, description="", location=""):
    service = get_calendar_service()

    event_body = {
        "summary": summary,
        "description": description,
        "location": location,
        "start": {
            "dateTime": start_time
        },
        "end": {
            "dateTime": end_time
        }
    }

    event = service.events().insert(
        calendarId="primary",
        body=event_body
    ).execute()

    return format_event(event)


def update_event(
    event_id,
    summary=None,
    start_time=None,
    end_time=None,
    description=None,
    location=None
):
    service = get_calendar_service()

    event = service.events().get(
        calendarId="primary",
        eventId=event_id
    ).execute()

    if summary is not None:
        event["summary"] = summary

    if description is not None:
        event["description"] = description

    if location is not None:
        event["location"] = location

    if start_time is not None:
        event["start"] = {"dateTime": start_time}

    if end_time is not None:
        event["end"] = {"dateTime": end_time}

    updated_event = service.events().update(
        calendarId="primary",
        eventId=event_id,
        body=event
    ).execute()

    return format_event(updated_event)


def delete_event(event_id):
    service = get_calendar_service()

    service.events().delete(
        calendarId="primary",
        eventId=event_id
    ).execute()

    return {
        "success": True,
        "message": "Event deleted successfully",
        "event_id": event_id
    }
