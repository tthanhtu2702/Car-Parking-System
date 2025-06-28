import unittest
from datetime import datetime
from decimal import Decimal
from models.car_parking import CarParking
from services.fee_calculator import calculate_payment_fee


class TestFeeCalculator(unittest.TestCase):

    def test_fee_on_weekday_regular_user(self):
        # Arrange: simulate Monday 9:00 AM to 11:00 AM (2 hours)
        arrival_time = datetime.strptime("2025-06-23 09:00:00", "%Y-%m-%d %H:%M:%S")  # Monday
        leaving_time = datetime.strptime("2025-06-23 11:00:00", "%Y-%m-%d %H:%M:%S")

        # CarParking(f"{arrival_time}:00", car_identity, frequent_parking_number)
        car_parking = CarParking(
            arrival_time=arrival_time,
            car_identity="63B-27101",
            frequent_parking_number=None,
        )
        car_parking.is_valid_fpn = "False"  # Regular user (not frequent)

        # Act
        fee = calculate_payment_fee(car_parking, leaving_time)

        # Assert: 2 weekday hours → 2 * $10.00 = $20.00
        expected_fee = Decimal("20.00")
        self.assertEqual(fee, expected_fee)

    def test_fee_on_weekday_frequent_user(self):
        arrival_time = datetime.strptime("2025-06-24 10:00:00", "%Y-%m-%d %H:%M:%S")  # Tuesday
        leaving_time = datetime.strptime("2025-06-24 13:00:00", "%Y-%m-%d %H:%M:%S")  # 3 hours

        car_parking = CarParking(
            arrival_time=arrival_time,
            car_identity="51A-56789",
            frequent_parking_number="12345",
        )
        car_parking.is_valid_fpn = "True"  # Frequent user

        # 2 hours at 10% off + 1 extra hour at double rate and 10% off
        expected_fee = (Decimal("10.00") * 2 * Decimal("0.90")) + (Decimal("10.00") * 2 * Decimal("0.90"))
        fee = calculate_payment_fee(car_parking, leaving_time)

        self.assertEqual(fee, round(expected_fee, 2))

if __name__ == "__main__":
    unittest.main()
