import sqlite3
from datetime import datetime

# -----------------------------
# Database setup
# -----------------------------
conn = sqlite3.connect("blood_bank.db")
cursor = conn.cursor()

# Create tables if not exist
cursor = conn.cursor(
    
cursor.execute("""
CREATE TABLE IF NOT EXISTS donors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
@@ -36,10 +32,6 @@

conn.commit()

# -----------------------------
# Functions
# -----------------------------

def add_donor():
    name = input("Enter name: ")
    age = int(input("Enter age: "))
@@ -80,10 +72,6 @@ def issue_blood():
    else:
        print("❌ Not enough stock.")

# -----------------------------
# Main Menu
# -----------------------------

def main():
    while True:
        print("\n=== Blood Bank Management ===")
