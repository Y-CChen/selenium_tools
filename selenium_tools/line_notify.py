from requests import request

_LINE_NOTIFY_MESSAGE_MAX_LEN = 950


def line_notify(message, access_token):
    while message:
        remaining_start = len(message)
        notifying_message = message[: _LINE_NOTIFY_MESSAGE_MAX_LEN + 1]
        if len(notifying_message) > _LINE_NOTIFY_MESSAGE_MAX_LEN:
            rindex = notifying_message.rfind("\n")
            notifying_message = notifying_message[:rindex]
            remaining_start = rindex + 1 if rindex != -1 else _LINE_NOTIFY_MESSAGE_MAX_LEN
        _line_notify(notifying_message, access_token)
        message = message[remaining_start:]


def _line_notify(message, access_token):
    url = "https://notify-api.line.me/api/notify"
    payload = "message=\n{}".format(message)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Authorization": "Bearer {}".format(access_token),
        "Host": "notify-api.line.me",
    }
    response = request("POST", url, data=payload.encode("utf-8"), headers=headers)
    return response
