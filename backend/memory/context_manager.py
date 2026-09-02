conversation_context = {
    "last_email": None,
    "last_event": None,
    "last_action": None,
    "pending_cancellation": None
}


def set_last_email(email):
    conversation_context["last_email"] = email


def get_last_email():
    return conversation_context["last_email"]


def set_last_event(event):
    conversation_context["last_event"] = event


def get_last_event():
    return conversation_context["last_event"]


def set_last_action(action):
    conversation_context["last_action"] = action


def set_pending_cancellation(data):
    conversation_context["pending_cancellation"] = data


def get_pending_cancellation():
    return conversation_context["pending_cancellation"]


def clear_pending_cancellation():
    conversation_context["pending_cancellation"] = None


def get_context():
    return conversation_context
