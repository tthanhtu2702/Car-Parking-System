"""Main CLI entry point for the Car Parking Service application.

This module defines the command-line interface (CLI) using Typer, enabling users
to interact with the system to park cars, pick up cars, and view parking history.
"""

import typer
from handlers.parking_handler import handle_parking
from handlers.pickup_handler import handle_pickup
from handlers.history_handler import handle_history

app = typer.Typer()


@app.command()
def park(
    car_id: str = typer.Option(None, "--car-id", help="Car identity (e.g., 63B-27101)"),
    time: str = typer.Option(None, "--time", help="Arrival time (e.g., 2025-06-27 18:30)"),
    fpn: str = typer.Option(None, "--fpn", help="Frequent parking number (e.g., 12345)"),
):
    """Park a car (interactive or via CLI)."""
    handle_parking(car_identity=car_id, arrival_time=time, frequent_parking_number=fpn)


@app.command()
def pickup(
    car_id: str = typer.Option(None, "--car-id", help="Car identity (e.g., 63B-27101)"),
    time: str = typer.Option(None, "--time", help="Leaving time (e.g., 2025-06-27 18:30)"),
):
    """Pick up a car (interactive or via CLI)."""
    handle_pickup(car_identity=car_id, leaving_time=time)

@app.command()
def history(
    car_id: str = typer.Option(None, "--car-id", help="Car identity (e.g., 63B-27101)")
):
    """View parking history (interactive or via CLI)."""
    handle_history(car_identity=car_id)


def run_cli():
    """Run the Car Parking Service CLI application."""
    app()


if __name__ == "__main__":
    run_cli()

# Sample CLI
# python main_cli.py park
# python main_cli.py pickup
# python main_cli.py history

# python main_cli.py park --car-id 63B-27101 --time "2025-06-28 09:00" --fpn 12345
# python main_cli.py pickup --car-id 63B-27101 --time "2025-06-28 11:30"
# python main_cli.py history --car-id 63B-27101
