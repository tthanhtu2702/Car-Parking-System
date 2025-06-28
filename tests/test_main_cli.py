from typer.testing import CliRunner
from main_cli import app

runner = CliRunner()

def test_parking_cli_with_arguments():
    result = runner.invoke(app, [
        "park",
        "--car-id", "63B-27101",
        "--arrival-time", "2025-06-28 09:00",
        "--frequent-parking-number", "12345"
    ])
    assert result.exit_code == 0
    assert "successfully parked" in result.stdout.lower()

def test_pickup_cli_with_arguments():
    result = runner.invoke(app, [
        "pickup",
        "--car-id", "63B-27101",
        "--leaving-time", "2025-06-28 11:30"
    ])
    assert result.exit_code == 0
    assert "successfully pickup" in result.stdout.lower()

def test_history_cli_with_arguments():
    result = runner.invoke(app, [
        "history",
        "--car-id", "63B-27101"
    ])
    assert result.exit_code == 0
    assert "parking history" in result.stdout.lower()

def test_parking_cli_without_arguments():
    result = runner.invoke(app, ["park"], input="63B-27101\n2025-06-28 09:00\n12345\n")
    assert result.exit_code == 0
    assert "successfully parked" in result.stdout.lower()

def test_pickup_cli_without_arguments():
    result = runner.invoke(app, ["pickup"], input="63B-27101\n2025-06-28 11:30\n100\n")
    assert result.exit_code == 0
    assert "successfully pickup" in result.stdout.lower()

def test_history_cli_without_arguments():
    result = runner.invoke(app, ["history"], input="63B-27101\n")
    assert result.exit_code == 0
    assert "parking history" in result.stdout.lower()

# Run the tests:
# pytest test_main_cli.py
