"""Module for calculating parking fees."""

from datetime import datetime, timedelta
from decimal import Decimal
import math
from utils.colors import RED, RESET
from models.car_parking import CarParking


def calculate_payment_fee(parked_car: CarParking, leaving_time: datetime) -> Decimal | None:
    """Calculate the total parking fee for a car based on arrival and leaving time.

    Args:
        parked_car (CarParking): The parked car object containing arrival time and frequent parking info.
        leaving_time (datetime): The time when the car is leaving.

    Returns:
        Decimal | None: The total fee rounded to 2 decimal places, or None if invalid.
    """
    if leaving_time < parked_car.arrival_time:
        print(RED + "Leaving time cannot be earlier than arrival time!" + RESET)
        return None

    time_periods = __calculate_hours_between(parked_car.arrival_time, leaving_time)
    total_fee = Decimal("0.00")

    discount_afternoon = Decimal("0.90") if parked_car.is_valid_fpn != "False" else Decimal("1.00")
    discount_other = Decimal("0.50") if parked_car.is_valid_fpn != "False" else Decimal("1.00")

    for day in time_periods:
        weekday = day["dayOfWeek"]
        h_08_17 = day["hours_from_08h_to_17h"]
        h_17_00 = day["hours_from_17h_to_00h"]
        h_00_08 = day["hours_from_00h_to_08h"]

        match weekday:
            case "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday":
                total_fee += __weekday_rate(h_08_17, 2, Decimal("10.00"), discount_afternoon)
            case "Saturday":
                total_fee += __weekday_rate(h_08_17, 4, Decimal("3.00"), discount_afternoon)
            case "Sunday":
                total_fee += __weekday_rate(h_08_17, 8, Decimal("2.00"), discount_afternoon)

        total_fee += __calculate_fee_morning_evening(h_00_08, h_17_00, discount_other)

    return round(total_fee, 2)


def __weekday_rate(hours: int, free_limit: int, base_rate: Decimal, discount: Decimal) -> Decimal:
    """Calculate weekday or weekend fee for 08h to 17h time block."""
    if hours <= free_limit:
        return hours * base_rate * discount
    base_fee = free_limit * base_rate * discount
    extra_fee = (hours - free_limit) * base_rate * 2 * discount
    return base_fee + extra_fee


def __calculate_fee_morning_evening(
    h_00_08: int, h_17_00: int, discount: Decimal
) -> Decimal:
    """Calculate the fee for morning and evening hours."""
    fee = h_17_00 * Decimal("5.00") * discount
    if h_00_08 > 0:
        fee += Decimal("20.00") * discount
    return fee


def __calculate_hours_between(arrival: datetime, leaving: datetime) -> list[dict]:
    """Breaks parking time into days and calculates hours spent in defined time ranges."""
    result = []
    blocks = [
        ("hours_from_08h_to_17h", 8, 17),
        ("hours_from_17h_to_00h", 17, 0),
        ("hours_from_00h_to_08h", 0, 8)
    ]

    current = arrival
    while current < leaving:
        day_summary = {
            "date": current.strftime("%Y-%m-%d"),
            "dayOfWeek": current.strftime("%A")
        }

        for block_name, start_h, end_h in blocks:
            start = current.replace(hour=start_h, minute=0, second=0)
            end = current.replace(hour=end_h, minute=0, second=0)
            if end_h == 0:
                end += timedelta(days=1)

            clipped_start = max(start, arrival)
            clipped_end = min(end, leaving)

            delta_hours = math.ceil(max(0, (clipped_end - clipped_start).total_seconds() / 3600))
            day_summary[block_name] = delta_hours

        result.append(day_summary)
        current += timedelta(days=1)

    return result
