from decimal import Decimal
from typing import NamedTuple


class PaymentBalance(NamedTuple):
    """Represents the available credit balance associated with a car."""
    car_identity: str
    available_credit: Decimal
