from datetime import date, timedelta
import calendar

def get_week_range():
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    return start_of_week, end_of_week

def get_month_range():
    today = date.today()
    start_of_month = date(today.year, today.month, 1)
    last_day = calendar.monthrange(today.year, today.month)[1]
    end_of_month = date(today.year, today.month, last_day)

    return start_of_month, end_of_month