"""Handler for querying car parking history."""

from typing import Optional
from utils.colors import RED, RESET, GREEN
from utils.history_writer import (
    show_payment_history_to_console,
    write_payment_history_to_file
)
from services import parking_service as _parking_service

def handle_history(car_identity: Optional[str] = None) -> None:
    """Handle car history query (supports CLI arguments or interactive mode)."""
    print("Welcome to CAR HISTORY QUERY. Please provide the information below (Ctrl + C to quit)")

    while True:
        try:
            if not car_identity:
                car_identity = input("> Please input car identity (e.g., 63B-27101): ").strip()

            if not car_identity:
                print(RED + "Car identity is empty." + RESET)
                car_identity = None
                continue

            parking_histories = _parking_service.get_parking_histories(car_identity)
            if not parking_histories:
                print(RED + "The provided car identity is not found or invalid." + RESET)
                car_identity = None
                continue

            payment_balance = _parking_service.get_payment_balance(car_identity)

            show_payment_history_to_console(car_identity, payment_balance, parking_histories)
            write_payment_history_to_file(car_identity, payment_balance, parking_histories)
            print(GREEN + f"The result has been saved." + RESET)
            break

        except KeyboardInterrupt:
            print("\n" + GREEN + "Operation cancelled by user." + RESET)
            break
        except Exception as e:
            print(RED + str(e) + RESET)
            break
