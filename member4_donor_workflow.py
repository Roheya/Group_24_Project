"""
Member 4 Module: Donor Workflow, Listing, and Reporting
Period Poverty Advocacy Platform
"""

import csv
import sqlite3

DB_NAME = "herperiod.db"


def connect_db():
    """Establishes connection to the shared SQLite database."""
    return sqlite3.connect(DB_NAME)


def initialize_db():
    """Ensures necessary database tables exist."""
    conn = connect_db()
    cursor = conn.cursor()

    # Table for school impact data
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS schools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            population INTEGER,
            girls_affected INTEGER,
            days_missed REAL,
            pad_cost REAL DEFAULT 1000.0,
            days_lost REAL,
            annual_cost REAL
        )
    """
    )

    # Table for donor pledges
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pledges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_name TEXT NOT NULL,
            school_name TEXT NOT NULL,
            pledge_amount REAL NOT NULL,
            pledge_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    conn.commit()
    conn.close()


def get_all_schools():
    """Fetch all school records from the database."""
    initialize_db()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, population, girls_affected, days_missed, pad_cost, days_lost, annual_cost FROM schools"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def record_pledge(donor_name, school_name, pledge_amount):
    """Store donor pledge details into the SQLite database."""
    initialize_db()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO pledges (donor_name, school_name, pledge_amount) VALUES (?, ?, ?)",
        (donor_name, school_name, pledge_amount),
    )
    conn.commit()
    conn.close()


def view_all_schools_impact():
    """07. Display list of schools with impact summary."""
    schools = get_all_schools()

    if not schools:
        print("\nNo registered schools found in the database.")
        return

    print("\nAll Registered Schools: Impact Overview")
    for school in schools:
        name, population, girls, days_missed, pad_cost, days_lost, annual_cost = (
            school
        )
        print(f"\nImpact Summary: {name}")
        print(f"Girls affected yearly: {girls}")
        print(f"School days lost     : {days_lost:.1f} days/year")
        print(f"Estimated annual cost: {annual_cost:,.2f} RWF")


def pledge_to_school(donor_name, default_pledge):
    """Allow donors to select a school and make/record a pledge."""
    schools = get_all_schools()

    if not schools:
        print("\nNo schools available to pledge to.")
        return

    print("\nAvailable schools:")
    for idx, school in enumerate(schools, 1):
        print(f"{idx}. {school[0]}")

    try:
        choice = int(input("Select a school by number: "))
        if 1 <= choice <= len(schools):
            selected_school = schools[choice - 1][0]

            use_default = (
                input(
                    f"Use your original pledge amount of {default_pledge:,.2f}? (yes/no): "
                )
                .strip()
                .lower()
            )

            if use_default in ["yes", "y"]:
                amount = default_pledge
            else:
                amount = float(input("Enter custom pledge amount (RWF): "))

            record_pledge(donor_name, selected_school, amount)
            print(
                f"Pledge of {amount:,.2f} RWF recorded for {selected_school}. Thank you!"
            )
        else:
            print("Invalid school selection.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")


def list_and_export_report():
    """08. Formatted Table display and CSV export."""
    schools = get_all_schools()

    if not schools:
        print("\nNo school data available for reporting.")
        return

    # Table Display
    print("\n" + "=" * 95)
    print(
        f"{'School':<22} | {'Population':<10} | {'Girls Affected':<14} | {'Days Missed':<11} | {'Pad Cost':<10} | {'Days Lost':<10} | {'Annual Cost (RWF)':<15}"
    )
    print("=" * 95)

    for school in schools:
        name, pop, girls, missed, pad, lost, cost = school
        print(
            f"{name:<22} | {pop:<10} | {girls:<14} | {missed:<11.1f} | {pad:<10.2f} | {lost:<10.1f} | {cost:<15.2f}"
        )
    print("=" * 95)

    # CSV Export prompt
    export = (
        input("\nWould you like to export this report to a CSV file? (yes/no): ")
        .strip()
        .lower()
    )

    if export in ["yes", "y"]:
        filename = "period_poverty_report.csv"
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "School",
                    "Population",
                    "Girls Affected",
                    "Days Missed",
                    "Pad Cost (RWF)",
                    "Days Lost",
                    "Annual Cost (RWF)",
                ]
            )
            for school in schools:
                writer.writerow(school)
        print(f"Report exported successfully to '{filename}'.")


def donor_workflow():
    """07 & 08. Main Donor Workflow function."""
    print("\n[07] Donor Workflow")

    donor_name = input("Enter your name: ").strip()
    try:
        pledge_amount = float(input("Enter your pledge amount (RWF): "))
    except ValueError:
        pledge_amount = 0.0

    print(
        f"\nWelcome, {donor_name}. Thank you for considering a pledge of {pledge_amount:,.2f} RWF."
    )

    while True:
        print("\n--- Donor Menu ---")
        print("1. View all schools and their impact")
        print("2. Pledge/donate to a specific school")
        print("3. List & export report")
        print("4. Log out")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            view_all_schools_impact()
        elif choice == "2":
            pledge_to_school(donor_name, pledge_amount)
        elif choice == "3":
            list_and_export_report()
        elif choice == "4":
            print("Logging out of donor session.")
            break
        else:
            print("Invalid choice. Please select 1-4.")


def seed_sample_data():
    """Populates default sample data matching requirements with 1000 RWF pad pricing."""
    initialize_db()
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM schools")

    # Sample schools based on prompt specs using standard 1000 RWF pad pricing reference
    sample_schools = [
        ("Greenfield Academy", 500, 300, 5.0, 1000.0, 1500.0, 36000.00),
        ("Riverside High School", 800, 420, 4.0, 1000.0, 1680.0, 60480.00),
    ]

    cursor.executemany(
        "INSERT INTO schools (name, population, girls_affected, days_missed, pad_cost, days_lost, annual_cost) VALUES (?, ?, ?, ?, ?, ?, ?)",
        sample_schools,
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    seed_sample_data()
    donor_workflow()