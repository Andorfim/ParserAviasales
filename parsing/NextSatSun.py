"""
Класс для определения ближайших выходных
"""

from datetime import date, timedelta


class NextSatSun:

    def __init__(self) -> None:
        pass

    def proceed(current_date):
        
        weekday = current_date.weekday()
        
        days_to_saturday = 5 - weekday if weekday < 5 else 12 - weekday
        
        days_to_sunday = 6 - weekday if weekday < 6 else 13 - weekday
        
        next_saturday = current_date + timedelta(days=days_to_saturday)
        next_sunday = current_date + timedelta(days=days_to_sunday)
        
        return next_saturday, next_sunday