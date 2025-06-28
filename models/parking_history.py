from datetime import datetime
from decimal import Decimal
from typing import NamedTuple


class ParkingHistory(NamedTuple):
    """Represents a record of a car's parking session."""
    car_identity: str
    arrival_time: datetime
    leaving_time: datetime
    frequent_parking_number: int
    is_valid_fpn: bool
    parking_fee: Decimal
