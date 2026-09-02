from backend.tools.calendar_tools import (
    get_events,
    search_events,
    get_event,
    check_availability,
    create_event,
    update_event,
    delete_event
)


def get_upcoming_events(max_results=10):
    return get_events(max_results)


def search_calendar_events(query, max_results=10):
    return search_events(query, max_results)


def get_calendar_event(event_id):
    return get_event(event_id)


def check_calendar_availability(start_time, end_time):
    return check_availability(start_time, end_time)


def schedule_event(
    summary,
    start_time,
    end_time,
    description="",
    location=""
):
    availability = check_availability(start_time, end_time)

    if not availability["available"]:
        return {
            "success": False,
            "message": "You are not available during this time.",
            "busy_periods": availability["busy_periods"]
        }

    event = create_event(
        summary=summary,
        start_time=start_time,
        end_time=end_time,
        description=description,
        location=location
    )

    return {
        "success": True,
        "message": "Event created successfully.",
        "event": event
    }


def update_calendar_event(
    event_id,
    summary=None,
    start_time=None,
    end_time=None,
    description=None,
    location=None
):
    event = update_event(
        event_id=event_id,
        summary=summary,
        start_time=start_time,
        end_time=end_time,
        description=description,
        location=location
    )

    return {
        "success": True,
        "message": "Event updated successfully.",
        "event": event
    }


def cancel_calendar_event(event_id):
    result = delete_event(event_id)

    return {
        "success": True,
        "message": "Event cancelled successfully.",
        "event_id": result["event_id"]
    }
