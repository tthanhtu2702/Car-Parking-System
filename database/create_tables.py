import sqlite3

def initialize_database():
    """Create tables for the car parking system if not exists."""
    conn = sqlite3.connect("database/parktrack.db")

    # Create car_parkings table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS car_parkings (
            car_identity TEXT PRIMARY KEY NOT NULL,
            arrival_time DATETIME NOT NULL,
            leaving_time DATETIME NULL,
            frequent_parking_number INT NULL,
            is_valid_fpn BIT DEFAULT 0 NOT NULL
        );
    ''')
    print("Created 'car_parkings' table successfully...")

    # Create parking_histories table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS parking_histories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_identity TEXT NOT NULL,
            arrival_time DATETIME NOT NULL,
            leaving_time DATETIME NULL,
            frequent_parking_number INT NULL,
            is_valid_fpn BIT DEFAULT 0 NOT NULL,
            parking_fee DECIMAL NOT NULL
        );
    ''')
    print("Created 'parking_histories' table successfully...")

    # Create payment_balances table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS payment_balances (
            car_identity TEXT PRIMARY KEY NOT NULL,
            available_credit DECIMAL NOT NULL DEFAULT 0.00
        );
    ''')
    print("Created 'payment_balances' table successfully...")

    conn.close()

if __name__ == "__main__":
    initialize_database()
