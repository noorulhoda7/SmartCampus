import datetime


def date_today():
    return datetime.date.today().strftime("%Y-%m-%d")


def current_time():
    return datetime.datetime.now().strftime("%H:%M:%S")
