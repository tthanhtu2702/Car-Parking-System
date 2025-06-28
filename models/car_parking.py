from datetime import datetime
from typing import Optional
import re
from ultils.constants import DATE_TIME_FORMAT
from ultils.check_digit_utils import generate_mod11_digit

class CarParking:
    """Represents a car being parked in the system."""

    _arrival_time: datetime
    _leaving_time: Optional[datetime] = None
    _car_identity: str
    _frequent_parking_number: Optional[int] = None

    is_valid_fpn: bool = False
    errors: list[str] = []

    def __init__(
        self,
        arrival_time: str,
        car_identity: str,
        frequent_parking_number: Optional[str] = None,
        leaving_time: Optional[str] = None
    ):
        self.arrival_time = arrival_time
        self.car_identity = car_identity
        self.frequent_parking_number = frequent_parking_number
        self.leaving_time = leaving_time

    def __repr__(self) -> str:
        return (
            f"Car identity: {self.car_identity}. "
            f"Arrival time: {self.arrival_time}. "
            f"Frequent Parking Number: {self.frequent_parking_number}. "
            f"Is valid frequent parking number: {self.is_valid_fpn}. "
            f"Leaving time: {self.leaving_time}"
        )

    @property
    def arrival_time(self) -> datetime:
        return self._arrival_time

    @arrival_time.setter
    def arrival_time(self, at: str):
        if not at:
            self.errors.append('Arrival time cannot be empty')
            return
        try:
            date_obj = datetime.strptime(str(at), DATE_TIME_FORMAT)
            if date_obj > datetime.now():
                self.errors.append("Arrival time can't be in the future")
            else:
                self._arrival_time = date_obj
        except ValueError:
            self.errors.append('Arrival time is invalid')

    @property
    def leaving_time(self) -> Optional[datetime]:
        return self._leaving_time

    @leaving_time.setter
    def leaving_time(self, lt: Optional[str]):
        if not lt:
            return
        try:
            date_obj = datetime.strptime(str(lt), DATE_TIME_FORMAT)
            self._leaving_time = date_obj
        except ValueError:
            self.errors.append('Leaving time is invalid')

    @property
    def car_identity(self) -> str:
        return self._car_identity

    @car_identity.setter
    def car_identity(self, ci: str):
        if not ci:
            self.errors.append('Car identity cannot be empty')
            return
        if not self.validate_car_identity(ci):
            self.errors.append('Invalid car identity format')
            return
        self._car_identity = ci

    def validate_car_identity(self, ci: str) -> bool:
        pattern = r'^[0-9]{2}[A-Z]{1}-[0-9]{5}$'
        return re.match(pattern, ci) is not None

    @property
    def frequent_parking_number(self) -> Optional[str]:
        return self._frequent_parking_number

    @frequent_parking_number.setter
    def frequent_parking_number(self, fpn: Optional[str]):
        self.is_valid_fpn = False
        self._frequent_parking_number = fpn
        if not fpn or fpn == 'None':
            return
        if not self.validate_frequent_parking_number(fpn):
            self.errors.append('Invalid frequent parking number')
            return
        if generate_mod11_digit(fpn[:4]) == int(fpn[4:]):
            self.is_valid_fpn = True

    def validate_frequent_parking_number(self, fpn: str) -> bool:
        pattern = r'^[0-9]{5}$'
        return re.match(pattern, fpn) is not None
