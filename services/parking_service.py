"""This module handles CRUD Car Parking"""
from datetime import datetime
from decimal import Decimal
import sqlite3
from utils.constants import DATE_TIME_FORMAT
from models.car_parking import CarParking
from models.parking_history import ParkingHistory
from models.payment_balance import PaymentBalance
conn = sqlite3.connect("database/parktrack.db")

def get_car_parking(car_identity: any) -> CarParking:
    """GET car by id"""
    query = (
    "SELECT arrival_time, car_identity, frequent_parking_number, is_valid_fpn "
    "FROM car_parkings WHERE car_identity = ?")
    result = conn.execute(query, (car_identity,)).fetchone()
    if result is not None:
        car_parking = CarParking(result[0], result[1], str(result[2]))
        car_parking.is_valid_fpn = result[3]
        return car_parking
    return None

def save_car_parking(car_parking: CarParking) -> bool:
    """INSERT new car"""
    conn.execute(
    "INSERT INTO car_parkings (car_identity, arrival_time, frequent_parking_number, is_valid_fpn) "
    "VALUES (?, ?, ?, ?)",
    (
        car_parking.car_identity,
        car_parking.arrival_time,
        car_parking.frequent_parking_number if car_parking.frequent_parking_number else None,
        car_parking.is_valid_fpn,
    ))
    conn.commit()
    return True

def remove_car_parking(car_identity: any) -> bool:
    """DELETE a car"""
    query = "DELETE FROM car_parkings WHERE car_identity = ?"
    conn.execute(query, (car_identity,))
    conn.commit()
    return True

def save_parking_history(parking_history: ParkingHistory) -> bool:
    """INSERT Parking History"""
    print(f"parking_history: ${parking_history}")
    conn.execute(
    "INSERT INTO parking_histories (car_identity, arrival_time, leaving_time"
        ", frequent_parking_number, is_valid_fpn, parking_fee) "
    "VALUES (?, ?, ?, ?, ?, ?)",
    (
        parking_history.car_identity,
        parking_history.arrival_time,
        parking_history.leaving_time,
        parking_history.frequent_parking_number,
        parking_history.is_valid_fpn,
        safe_sql_value(parking_history.parking_fee)
    ))
    conn.commit()
    return True

def get_parking_histories(car_identity) -> list[ParkingHistory]:
    """GET list of Parking Histories"""
    query = (
    "SELECT car_identity, arrival_time, leaving_time, frequent_parking_number, "
    "is_valid_fpn, parking_fee "
    "FROM parking_histories "
    "WHERE car_identity = ? "
    "ORDER BY arrival_time DESC")
    results = conn.execute(query, (car_identity,)).fetchall()
    parking_histories: list[ParkingHistory] = []
    if results is not None:
        for result in results:
            parking_histories.append(
                    ParkingHistory(
                        result[0],
                        datetime.strptime(result[1], DATE_TIME_FORMAT),
                        datetime.strptime(result[2], DATE_TIME_FORMAT),
                        result[3],
                        result[4],
                        result[5]
                    )
                )
        return parking_histories
    return None

def save_payment_balance(payment_balance: PaymentBalance) -> bool:
    """INSERT Payment Balance"""
    query = (
        "INSERT INTO payment_balances (car_identity, available_credit) "
        "VALUES (?, ?)"
        )
    conn.execute(query, (payment_balance.car_identity, safe_sql_value(payment_balance.available_credit)))
    conn.commit()
    return True

def get_payment_balance(car_identity) -> PaymentBalance:
    """GET Payment Balance"""
    query = (
    "SELECT car_identity, available_credit "
    "FROM payment_balances "
    "WHERE car_identity = ?")
    result = conn.execute(query, (car_identity,)).fetchone()
    if result is not None:
        return PaymentBalance(car_identity=result[0], available_credit=result[1])
    return None

def update_payment_balance(payment_balance: PaymentBalance) -> bool:
    """UPDATE Payment Balance"""
    query = (
    "UPDATE payment_balances "
    "SET available_credit = ? "
    "WHERE car_identity = ?")
    conn.execute(
        query,
        (safe_sql_value(payment_balance.available_credit), payment_balance.car_identity))
    conn.commit()
    return True

def safe_sql_value(value):
    return float(value) if isinstance(value, Decimal) else value
