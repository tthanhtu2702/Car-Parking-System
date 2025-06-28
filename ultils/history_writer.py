"""Utility functions to display and export parking history information."""

from datetime import datetime
from decimal import Decimal
from ntpath import join
from os import makedirs
from ultils.constants import DATE_TIME_FILE_FORMAT, DATE_TIME_NEEDED_FORMAT
from ultils.colors import GREEN, RESET
from models.parking_history import ParkingHistory
from models.payment_balance import PaymentBalance


def show_payment_history_to_console(
    car_identity: str,
    payment_balance: PaymentBalance,
    parking_histories: list[ParkingHistory]
) -> None:
    """Display parking history and payment summary to the console."""
    total_payment = sum(history.parking_fee for history in parking_histories)
    available_credit = round(payment_balance.available_credit, 2) if payment_balance else Decimal("0.00")

    print(f"{'*' * 26} PARKING HISTORY - {car_identity} {'*' * 26}")
    print(f"   Total payment:        ${round(total_payment, 2)}")
    print(f"   Available credits:    ${available_credit}")
    print("   Parked Dates:")
    for history in parking_histories:
        start = history.arrival_time.strftime(DATE_TIME_NEEDED_FORMAT)
        end = history.leaving_time.strftime(DATE_TIME_NEEDED_FORMAT)
        print(f"        {start} - {end}  ${history.parking_fee}")
    print(f"{'*' * 26} PARKING HISTORY - {car_identity} {'*' * 26}")


def write_payment_history_to_file(
    car_identity: str,
    payment_balance: PaymentBalance,
    parking_histories: list[ParkingHistory]
) -> None:
    """Write parking history and payment summary to a file."""
    total_payment = sum(history.parking_fee for history in parking_histories)
    available_credit = round(payment_balance.available_credit, 2) if payment_balance else Decimal("0.00")
    file_path = generate_history_file_path(car_identity)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"Total payment: ${round(total_payment, 2)}\n")
        file.write(f"Available credits: ${available_credit}\n")
        file.write("Parked Dates:\n")
        for history in parking_histories:
            start = history.arrival_time.strftime(DATE_TIME_NEEDED_FORMAT)
            end = history.leaving_time.strftime(DATE_TIME_NEEDED_FORMAT)
            file.write(f"\t{start} - {end}  ${history.parking_fee}\n")

    print(GREEN + f"The result has been saved to file: {file_path}" + RESET)

def generate_history_file_path(car_identity: str) -> str:
    """Generate a unique file path for exporting a car's parking history"""
    export_dir = "exports"
    makedirs(export_dir, exist_ok=True)

    #filename = f"{car_identity}_{datetime.now().strftime(DATE_TIME_FILE_FORMAT)}.txt"
    filename = f"{car_identity}.txt"
    return join(export_dir, filename)
