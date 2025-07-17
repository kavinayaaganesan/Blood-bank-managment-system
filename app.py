import sqlite3
from datetime import datetime

# Database connection
conn = sqlite3.connect("blood_bank.db")
cursor = conn.cursor()

# Create tables if not exists
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
conn.commit()

# Utility function
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# Add Donor
def add_donor():
    name = input("Enter name: ")
    try:
        age = int(input("Enter age: "))
    except ValueError:
        print("❌ Invalid age.")
        return
    gender = input("Enter gender: ")
    blood_group = input("Enter blood group: ").upper()
    phone = input("Enter phone: ")
    address = input("Enter address: ")
    last_donation_date = input("Last donation date (YYYY-MM-DD): ")
    while not is_valid_date(last_donation_date):
        print("❌ Invalid date format.")
        last_donation_date = input("Last donation date (YYYY-MM-DD): ")

    with conn:
        conn.execute("""
        INSERT INTO donors (name, age, gender, blood_group, phone, address, last_donation_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, age, gender, blood_group, phone, address, last_donation_date))
    print("✅ Donor added.")

# Update Stock after Donation
def update_stock_after_donation():
    blood_group = input("Enter blood group donated: ").upper()
    try:
        units = int(input("Enter units donated: "))
    except ValueError:
        print("❌ Invalid units.")
        return
    cursor.execute("SELECT units_available FROM blood_stock WHERE blood_group = ?", (blood_group,))
    record = cursor.fetchone()
    if record:
        with conn:
            conn.execute("UPDATE blood_stock SET units_available = units_available + ? WHERE blood_group = ?", (units, blood_group))
    else:
        with conn:
            conn.execute("INSERT INTO blood_stock (blood_group, units_available) VALUES (?, ?)", (blood_group, units))
    print("✅ Stock updated.")

# View Blood Stock
def view_stock():
    cursor.execute("SELECT * FROM blood_stock")
    stock = cursor.fetchall()
    print("\n=== Current Blood Stock ===")
    if stock:
        for row in stock:
            print(f"{row[0]}: {row[1]} units available")
    else:
        print("No stock data available.")

# Issue Blood
def issue_blood():
    blood_group = input("Enter blood group required: ").upper()
    try:
        units_needed = int(input("Enter units needed: "))
    except ValueError:
        print("❌ Invalid units.")
        return
    cursor.execute("SELECT units_available FROM blood_stock WHERE blood_group = ?", (blood_group,))
    stock = cursor.fetchone()
    if stock and stock[0] >= units_needed:
        with conn:
            conn.execute("UPDATE blood_stock SET units_available = units_available - ? WHERE blood_group = ?", (units_needed, blood_group))
        print("✅ Blood issued.")
    else:
        print("❌ Not enough stock.")

# View Donors
def view_donors():
    cursor.execute("SELECT id, name, blood_group, last_donation_date FROM donors ORDER BY id DESC")
    donors = cursor.fetchall()
    print("\n=== Donor List ===")
    if donors:
        for donor in donors:
            print(f"ID: {donor[0]}, Name: {donor[1]}, Blood Group: {donor[2]}, Last Donation: {donor[3]}")
    else:
        print("No donors found.")

# Search Donors by Blood Group
def search_donor_by_blood_group():
    blood_group = input("Enter blood group to search: ").upper()
    cursor.execute("SELECT id, name, phone, last_donation_date FROM donors WHERE blood_group = ?", (blood_group,))
    donors = cursor.fetchall()
    print(f"\n=== Donors with blood group {blood_group} ===")
    if donors:
        for donor in donors:
            print(f"ID: {donor[0]}, Name: {donor[1]}, Phone: {donor[2]}, Last Donation: {donor[3]}")
    else:
        print("No donors found.")

# Delete Donor
def delete_donor():
    try:
        donor_id = int(input("Enter donor ID to delete: "))
    except ValueError:
        print("❌ Invalid ID.")
        return
    cursor.execute("SELECT * FROM donors WHERE id = ?", (donor_id,))
    donor = cursor.fetchone()
    if donor:
        confirm = input(f"Are you sure you want to delete donor {donor[1]}? (y/n): ").lower()
        if confirm == "y":
            with conn:
                conn.execute("DELETE FROM donors WHERE id = ?", (donor_id,))
            print("✅ Donor deleted.")
        else:
            print("Deletion cancelled.")
    else:
        print("❌ Donor not found.")

# View Low Stock Alerts
def view_low_stock():
    threshold = 5
    cursor.execute("SELECT blood_group, units_available FROM blood_stock WHERE units_available < ?", (threshold,))
    low_stock = cursor.fetchall()
    print("\n=== Low Stock Alerts (below 5 units) ===")
    if low_stock:
        for stock in low_stock:
            print(f"{stock[0]}: {stock[1]} units remaining")
    else:
        print("All stocks are sufficient.")

# Show Statistics
def show_statistics():
    cursor.execute("SELECT COUNT(*) FROM donors")
    total_donors = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(units_available) FROM blood_stock")
    total_units = cursor.fetchone()[0] or 0
    print("\n=== Blood Bank Statistics ===")
    print(f"Total Donors: {total_donors}")
    print(f"Total Blood Units in Stock: {total_units}")

# Main Menu
def main():
    while True:
        print("\n=== Blood Bank Management ===")
        print("1. Add Donor")
        print("2. Update Stock After Donation")
        print("3. View Blood Stock")
        print("4. Issue Blood")
        print("5. View Donors")
        print("6. Search Donor by Blood Group")
        print("7. Delete Donor")
        print("8. View Low Stock Alerts")
        print("9. Show Statistics")
        print("10. Exit")

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
            search_donor_by_blood_group()
        elif choice == "7":
            delete_donor()
        elif choice == "8":
            view_low_stock()
        elif choice == "9":
            show_statistics()
        elif choice == "10":
            print("Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    try:
        main()
    finally:
        conn.close()
