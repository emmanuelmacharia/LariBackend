from dateutil.relativedelta import relativedelta

def format_duration(start_time, end_time):
    duration = relativedelta(end_time, start_time)
    if duration.years >= 1:
        timeline = f"{duration.years} year(s), {duration.months} month(s)"
    elif duration.months >= 1:
        timeline = f"{duration.months} month(s), {duration.weeks} week(s)"
    elif duration.weeks >= 1:
        timeline = f"{duration.weeks} month(s), {duration.days} day(s)"
    else:
        timeline = f"{duration.days} day(s)"

    return timeline