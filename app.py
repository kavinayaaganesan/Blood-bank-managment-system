import sqlite3
from datetime import datetime

# Database connection
conn = sqlite3.connect("blood_bank.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS donors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    blood_group TEXT,
    phone TEXT,
    address TEXT,
    last_donation_date TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS blood_stock (
    blood_group TEXT PRIMARY KEY,
    units_available INTEGER
)
""")

# Initialize stock for all blood groups
blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
for bg in blood_groups:
    cursor.execute("INSERT OR IGNORE INTO blood_stock (blood_group, units_available) VALUES (?, ?)", (bg, 0))

conn.commit()

def add_donor():
    name = input("Enter name: ")
    try:
        age = int(input("Enter age: "))
    except ValueError:
        print("❌ Invalid age. Must be a number.")
        return
    gender = input("Enter gender: ")
    blood_group = input("Enter blood group: ").upper()
    phone = input("Enter phone: ")
    address = input("Enter address: ")
    last_donation_date = input("Last donation date (YYYY-MM-DD): ")
    try:
        datetime.strptime(last_donation_date, "%Y-%m-%d")
    except ValueError:
        print("❌ Invalid date format.")
        return

    with conn:
        conn.execute("""
        INSERT INTO donors (name, age, gender, blood_group, phone, address, last_donation_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, age, gender, blood_group, phone, address, last_donation_date))
    print("✅ Donor added successfully.")

def update_stock_after_donation():
    blood_group = input("Enter blood group donated: ").upper()
    try:
        units = int(input("Enter units donated: "))
    except ValueError:
        print("❌ Units must be a number.")
        return
    with conn:
        conn.execute("UPDATE blood_stock SET units_available = units_available + ? WHERE blood_group = ?", (units, blood_group))
    print("✅ Stock updated.")

def view_stock():
    cursor.execute("SELECT * FROM blood_stock")
    print("\n=== Current Blood Stock ===")
    for row in cursor.fetchall():
        print(f"{row[0]}: {row[1]} units available")

def issue_blood():
    blood_group = input("Enter blood group required: ").upper()
    try:
        units_needed = int(input("Enter units needed: "))
    except ValueError:
        print("❌ Units must be a number.")
        return
    cursor.execute("SELECT units_available FROM blood_stock WHERE blood_group = ?", (blood_group,))
    stock = cursor.fetchone()
    if stock and stock[0] >= units_needed:
        with conn:
            conn.execute("UPDATE blood_stock SET units_available = units_available - ? WHERE blood_group = ?", (units_needed, blood_group))
        print("✅ Blood issued.")
    else:
        print("❌ Not enough stock.")

def view_donors():
    cursor.execute("SELECT id, name, blood_group, last_donation_date FROM donors ORDER BY id DESC")
    donors = cursor.fetchall()
    print("\n=== Donor List ===")
    if donors:
        for donor in donors:
            print(f"ID: {donor[0]}, Name: {donor[1]}, Blood Group: {donor[2]}, Last Donation: {donor[3]}")
    else:
        print("No donors found.")

def main():
    while True:
        print("\n=== Blood Bank Management ===")
        print("1. Add Donor")
        print("2. Update Stock After Donation")
        print("3. View Blood Stock")
        print("4. Issue Blood")
        print("5. View Donors")
        print("6. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            add_donor()
        elif choice == "2":
            update_stock_after_donation()
        elif choice == "3":
            view_stock()
        elif choice == "4":
            issue_blood()
        elif choice == "5":
            view_donors()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
    conn.close()
