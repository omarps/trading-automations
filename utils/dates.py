import sys
import pandas_market_calendars as mcal
from datetime import datetime, timedelta


def get_latest_trading_day():
    nyse = mcal.get_calendar('NYSE')
    today = datetime.now()
    schedule = nyse.schedule(start_date=today - timedelta(days=10), end_date=today)
    latest_trading_day = schedule.iloc[-1].name
    return latest_trading_day.strftime('%Y%m%d')


def get_latest_week_day():
    today = datetime.now()

    # Get Sunday of the current week
    sunday = today + timedelta(days=(6 - today.weekday()))

    return sunday.strftime('%Y%m%d')


def get_date_param(date_type="trading"):
    # Use the first command-line argument if provided
    if len(sys.argv) > 1:
        return sys.argv[1]

    # otherwise use the latest trading day
    if date_type == 'trading':
        date = get_latest_trading_day()
    else:
        date = get_latest_week_day()
    return date
