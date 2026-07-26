#!/usr/bin/python3
"""
Period Poverty Advocacy Platform
Integrated Version

Member 1 - Welcome Screen
Member 2 - School Registration
Member 3 - Calculations
Member 4 - Donor Workflow
"""

import sqlite3
import csv
from datetime import date

DATABASE = "herperiod.db"
SQL_FILE = "schools_records.sql"

# ============================================================
# WELCOME SCREEN (MEMBER 1)
# ============================================================

def welcome_message():
    print("\n" + "=" * 70)
    print("        PERIOD POVERTY ADVOCACY PLATFORM")
    print("=" * 70)
    print("Connecting Schools and Donors to End Period Poverty")
    print(
        "This platform allows schools to register impact data "
        "and donors to support schools in need."
    )


def role_selection():
    print("\nLogin As:")
    print("1. School")
    print("2. Donor")
    print("3. Exit")

    return input("\nEnter your choice (1-3): ").strip()


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def create_database():
    """
    Creates all required tables.
    Reads schools table from schools_records.sql
    Creates pledges table if it doesn't exist.
    """

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create Schools table

    with open(SQL_FILE, "r") as file:
        cursor.executescript(file.read())

    # Create Donor table

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pledges (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            donor_name TEXT NOT NULL,

            school_name TEXT NOT NULL,

            pledge_amount REAL NOT NULL,

            pledge_date TEXT DEFAULT CURRENT_TIMESTAMP

        )
    """)

    conn.commit()
    conn.close()


# ============================================================
# SCHOOL DATABASE FUNCTIONS
# ============================================================

def get_school_data(school_name):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM schools
        WHERE school_name = ?
        """,
        (school_name,)
    )

    result = cursor.fetchone()

    conn.close()

    return result


def save_school_data(
        school_name,
        population,
        girls_affected,
        days_missed,
        pad_cost,
        days_lost,
        annual_cost):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""

        INSERT OR REPLACE INTO schools(

            school_name,
            population,
            girls_affected,
            days_missed,
            pad_cost,
            days_lost,
            annual_cost,
            date_added

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        school_name,
        population,
        girls_affected,
        days_missed,
        pad_cost,
        days_lost,
        annual_cost,
        str(date.today())

    ))

    conn.commit()
    conn.close()


def display_schools_table():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            school_name,
            population,
            girls_affected,
            days_missed,
            pad_cost,
            days_lost,
            annual_cost,
            date_added

        FROM schools

    """)

    rows = cursor.fetchall()

    conn.close()

    print("\nCurrent Schools Database")
    print("-" * 120)

    print(
        f"{'School':<20}"
        f"{'Population':<12}"
        f"{'Girls':<12}"
        f"{'Days Missed':<15}"
        f"{'Pad Cost':<12}"
        f"{'Days Lost':<15}"
        f"{'Annual Cost':<18}"
        f"{'Date Added'}"
    )

    print("-" * 120)

    for row in rows:

        print(
            f"{row[0]:<20}"
            f"{row[1]:<12}"
            f"{row[2]:<12}"
            f"{row[3]:<15}"
            f"{row[4]:<12}"
            f"{row[5]:<15}"
            f"{row[6]:<18.2f}"
            f"{row[7]}"
        )


# ============================================================
# DONOR DATABASE FUNCTIONS
# ============================================================

def get_all_schools():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            school_name,
            population,
            girls_affected,
            days_missed,
            pad_cost,
            days_lost,
            annual_cost

        FROM schools

    """)

    schools = cursor.fetchall()

    conn.close()

    return schools


def record_pledge(
        donor_name,
        school_name,
        pledge_amount):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO pledges(

            donor_name,
            school_name,
            pledge_amount

        )

        VALUES (?, ?, ?)

    """, (

        donor_name,
        school_name,
        pledge_amount

    ))

    conn.commit()

    conn.close()
# ============================================================
# DONOR WORKFLOW (MEMBER 4)
# ============================================================

def view_all_schools_impact():
    """Display all registered schools and their impact."""

    schools = get_all_schools()

    if not schools:
        print("\nNo registered schools found.")
        return

    print("\n===============================")
    print(" REGISTERED SCHOOLS")
    print("===============================")

    for school in schools:

        name, population, girls, missed, pad, lost, cost = school

        print(f"\nSchool Name          : {name}")
        print(f"Population           : {population}")
        print(f"Girls Affected       : {girls}")
        print(f"Average Days Missed  : {missed}")
        print(f"Days Lost Per Year   : {lost}")
        print(f"Annual Cost          : {cost:,.2f} RWF")


def pledge_to_school(donor_name, default_amount):
    """Allow donor to select a school and make a pledge."""

    schools = get_all_schools()

    if not schools:
        print("\nNo schools available.")
        return

    print("\nAvailable Schools")

    for i, school in enumerate(schools, start=1):
        print(f"{i}. {school[0]}")

    try:

        choice = int(input("\nChoose a school: "))

        if choice < 1 or choice > len(schools):
            print("Invalid selection.")
            return

        school_name = schools[choice - 1][0]

        answer = input(
            f"\nUse your original pledge of "
            f"{default_amount:,.2f} RWF? (yes/no): "
        ).strip().lower()

        if answer == "yes":

            amount = default_amount

        else:

            amount = float(
                input("Enter new pledge amount (RWF): ")
            )

        record_pledge(
            donor_name,
            school_name,
            amount
        )

        print("\nPledge recorded successfully!")
        print(f"Donor : {donor_name}")
        print(f"School: {school_name}")
        print(f"Amount: {amount:,.2f} RWF")

    except ValueError:

        print("Invalid input.")


def list_and_export_report():
    """Display schools and optionally export CSV."""

    schools = get_all_schools()

    if not schools:
        print("\nNo schools available.")
        return

    print("\n" + "=" * 100)

    print(
        f"{'School':<22}"
        f"{'Population':<12}"
        f"{'Girls':<12}"
        f"{'Days Missed':<15}"
        f"{'Pad Cost':<12}"
        f"{'Days Lost':<15}"
        f"{'Annual Cost'}"
    )

    print("=" * 100)

    for school in schools:

        print(
            f"{school[0]:<22}"
            f"{school[1]:<12}"
            f"{school[2]:<12}"
            f"{school[3]:<15}"
            f"{school[4]:<12}"
            f"{school[5]:<15}"
            f"{school[6]:,.2f}"
        )

    export = input(
        "\nExport report to CSV? (yes/no): "
    ).strip().lower()

    if export == "yes":

        filename = "period_poverty_report.csv"

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "School",
                "Population",
                "Girls Affected",
                "Days Missed",
                "Pad Cost",
                "Days Lost",
                "Annual Cost"
            ])

            for school in schools:
                writer.writerow(school)

        print(f"\nReport exported as '{filename}'.")


def donor_workflow():
    """Main donor menu."""

    print("\n===============================")
    print(" DONOR PORTAL")
    print("===============================")

    donor_name = input("Enter your name: ").strip()

    try:

        pledge = float(
            input("Enter pledge amount (RWF): ")
        )

    except ValueError:

        pledge = 0

    while True:

        print("\n========== DONOR MENU ==========")
        print("1. View Schools")
        print("2. Donate to School")
        print("3. Export Report")
        print("4. View My Donations")
        print("5. Logout")

        choice = input("\nChoose an option: ")

        if choice == "1":

            view_all_schools_impact()

        elif choice == "2":

            pledge_to_school(
                donor_name,
                pledge
            )

        elif choice == "3":

            list_and_export_report()

        elif choice == "4":

            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    donor_name,
                    school_name,
                    pledge_amount,
                    pledge_date
                FROM pledges
                WHERE donor_name = ?
            """, (donor_name,))

            donations = cursor.fetchall()

            conn.close()

            if donations:

                print("\nYour Donations")

                for donation in donations:

                    print(
                        f"\nSchool : {donation[1]}"
                    )

                    print(
                        f"Amount : {donation[2]:,.2f} RWF"
                    )

                    print(
                        f"Date   : {donation[3]}"
                    )

            else:

                print("\nNo donations found.")

        elif choice == "5":

            print("\nLogging out...\n")

            break

        else:

            print("Invalid option.")
# ============================================================
# MAIN MENU
# ============================================================

def main():

    create_database()

    while True:

        welcome_message()

        choice = role_selection()

        if choice == "1":

            # School Registration
            school_registration()

        elif choice == "2":

            # Donor Portal
            donor_workflow()

        elif choice == "3":

            print("\nThank you for using the")
            print("Period Poverty Advocacy Platform.")
            print("Goodbye!\n")
            break

        else:

            print("\nInvalid choice.")
            print("Please enter 1, 2 or 3.\n")


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    main()
