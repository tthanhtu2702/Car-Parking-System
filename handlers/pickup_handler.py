"""Handler for car pickup process."""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from utils.colors import RED, RESET, GREEN, YELLOW
from utils.constants import DATE_TIME_FORMAT, DATE_TIME_NEEDED_FORMAT
from models.parking_history import ParkingHistory
from models.payment_balance import PaymentBalance
from services import parking_service as _parking_service
from services import fee_calculator as _fee_calculator

def handle_pickup(car_identity: Optional[str] = None, leaving_time: Optional[str] = None) -> None:
    """Handle car pickup (supports CLI arguments or interactive mode)."""
    print("Welcome to CAR PICKUP. Please provide the information below (Ctrl + C to quit)")

    while True:
        try:
            if not car_identity:
                car_identity = input("> Please input car identity (e.g., 63B-27101): ").strip()

            if not car_identity:
                print(RED + "Car identity is empty." + RESET)
                car_identity = None
                continue

            parked_car = _parking_service.get_car_parking(car_identity)
            if not parked_car:
                print(RED + "Invalid car identity or your car is not in the parking lot." + RESET)
                car_identity = None
                continue

            # Determine leaving time
            actual_leaving_time = datetime.now()
            if not leaving_time:
                temp = input(
                    "> Leaving time - example 2025-06-27 18:30 - (optional): "
                ).strip()
                if temp:
                    try:
                        actual_leaving_time = datetime.strptime(temp + ":00", DATE_TIME_FORMAT)
                    except ValueError:
                        print(
                            YELLOW
                            + f"Invalid time format. Using current datetime: {actual_leaving_time.strftime(DATE_TIME_NEEDED_FORMAT)}"
                            + RESET
                        )
            else:
                try:
                    actual_leaving_time = datetime.strptime(leaving_time + ":00", DATE_TIME_FORMAT)
                except ValueError:
                    print(
                        YELLOW
                        + f"Invalid time format. Using current datetime: {actual_leaving_time.strftime(DATE_TIME_NEEDED_FORMAT)}"
                        + RESET
                    )

            # Calculate payment fee
            payment_fee = _fee_calculator.calculate_payment_fee(parked_car, actual_leaving_time)
            if payment_fee is None:
                break

            print(f"=> Your parking fee is: ${payment_fee}")

            # Fetch balance
            payment_balance = _parking_service.get_payment_balance(car_identity)
            available_credit = (
                Decimal(payment_balance.available_credit) if payment_balance else Decimal("0.00")
            )

            # Prompt for payment amount
            payment_amount_input = __input_and_validate_payment_amount(payment_fee, available_credit)
            final_available_credit = payment_amount_input + available_credit - payment_fee

            # Save history
            parking_history = ParkingHistory(
                car_identity,
                parked_car.arrival_time,
                actual_leaving_time.strftime(DATE_TIME_FORMAT),
                parked_car.frequent_parking_number or 'NULL',
                parked_car.is_valid_fpn,
                float(payment_fee)  # use float to avoid sqlite Decimal issue
            )
            _parking_service.save_parking_history(parking_history)

            # Update or add balance
            updated_balance = PaymentBalance(car_identity, float(final_available_credit))
            if payment_balance:
                _parking_service.update_payment_balance(updated_balance)
            else:
                _parking_service.save_payment_balance(updated_balance)

            # Remove car from lot
            _parking_service.remove_car_parking(car_identity)

            print(GREEN + "Your car is successfully picked up." + RESET)
            break

        except KeyboardInterrupt:
            print("\n" + GREEN + "Operation cancelled by user." + RESET)
            break
        except Exception as e:
            print(RED + str(e) + RESET)
            break

def __input_and_validate_payment_amount(payment_fee: Decimal, available_credit: Decimal) -> Decimal:
    while True:
        try:
            # Validate payment amount input
            payment_amount = input("> Input your payment amount: ")
            if not payment_amount.replace(".", "", 1).isdigit():
                print(RED + "Invalid payment amount" + RESET)
                continue
            payment_amount_decimal = Decimal(payment_amount)
            if payment_amount_decimal + available_credit < payment_fee:
                print(RED + "Payment amount needs to be great or equal the payment fee" + RESET)
                continue
            return payment_amount_decimal
        except Exception as e:
            raise e
