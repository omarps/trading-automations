import sys
import pandas_market_calendars as mcal
from datetime import datetime, timedelta


def get_latest_trading_day():
    nyse = mcal.get_calendar('NYSE')
    today = datetime.now()
    schedule = nyse.schedule(start_date=today - timedelta(days=10), end_date=today)
    latest_trading_day = schedule.iloc[-1].name
    return latest_trading_day.strftime('%Y%m%d')


def get_date_param():
    # Use the first command-line argument if provided, otherwise use the latest trading day
    date = sys.argv[1] if len(sys.argv) > 1 else get_latest_trading_day()
    return date
