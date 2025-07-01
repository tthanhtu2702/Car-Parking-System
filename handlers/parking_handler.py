"""Handler for car parking process."""

from datetime import datetime
from utils.colors import RED, RESET, GREEN
from models.car_parking import CarParking
from services import parking_service as _parking_service

def handle_parking(
    car_identity: str = None,
    arrival_time: str = None,
    frequent_parking_number: str = None,
) -> None:
    """Handle car parking (supports CLI arguments or interactive mode)."""
    print("Welcome to CAR PARKING. Please provide the information below (Ctrl + C to quit)")

    while True:
        try:
            # Interactive input if CLI args not provided
            if not car_identity:
                car_identity = input("> Please input car identity (e.g., 63B-27101): ").strip()

            if not arrival_time:
                arrival_time = input("> Please input arrival time (e.g., 2025-06-27 18:30): ").strip()

            if frequent_parking_number is None:
                frequent_parking_number = input(
                    "> Please input frequent parking number if any (e.g., 12345): "
                ).strip()

            # Validation
            if not car_identity:
                print(RED + "Car identity is empty." + RESET)
                car_identity = None
                continue

            # Check if car is already parked
            if _parking_service.get_car_parking(car_identity):
                print(RED + "Invalid parking. Your car has already parked." + RESET)
                break

            # Create car parking instance
            car_parking = CarParking(f"{arrival_time}:00", car_identity, frequent_parking_number)

            if car_parking.errors:
                for error in car_parking.errors:
                    print(RED + error + RESET)
                car_parking.errors.clear()
                # Reset CLI values if interactive
                if not any([car_identity, arrival_time]):
                    car_identity, arrival_time = None, None
                continue

            # Save
            _parking_service.save_car_parking(car_parking)
            print(GREEN + "Your car is successfully parked." + RESET)
            break

        except KeyboardInterrupt:
            print("\n" + GREEN + "Operation cancelled by user." + RESET)
            break

        except Exception as e:
            print(RED + str(e) + RESET)
            break

