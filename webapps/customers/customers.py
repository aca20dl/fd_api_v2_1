from typing import List

from sqlalchemy.orm import Session
from datetime import datetime, time, timedelta
import numpy as np

def average_transactions_per_week(transaction_dates):
    # Parse the date strings into datetime objects
    parsed_dates = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f") for date in transaction_dates]

    # Find the minimum and maximum dates in the list
    min_date = min(parsed_dates)
    max_date = max(parsed_dates)

    # Calculate the duration between the minimum and maximum dates in weeks
    duration_weeks = (max_date - min_date).days / 7

    # Calculate the average number of transactions per week
    avg_transactions_per_week = len(transaction_dates) / duration_weeks

    return avg_transactions_per_week


def avg_time_frame(transaction_dates: List[str]) -> np.ndarray:
    # Parse the date strings into datetime objects
    parsed_dates = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f") for date in transaction_dates]

    # Extract the time of the day (in seconds) for each transaction
    times_of_day_seconds = [date.time().hour * 3600 + date.time().minute * 60 + date.time().second for date in parsed_dates]

    # Calculate the average time of the day in seconds
    avg_time_seconds = np.mean(times_of_day_seconds)

    # Convert the average time in seconds to a time object
    avg_time = time(hour=int(avg_time_seconds // 3600), minute=int((avg_time_seconds % 3600) // 60), second=int(avg_time_seconds % 60))

    # Calculate the start and end time of the 3-hour time period
    start_time = (datetime.combine(datetime.today(), avg_time) - timedelta(hours=1.5)).time()
    end_time = (datetime.combine(datetime.today(), avg_time) + timedelta(hours=1.5)).time()
    time_frame = [start_time, end_time]

    return time_frame


