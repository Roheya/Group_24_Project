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
=======
#!/usr/bin/python3
def welcome_message():
    print("HerPeriod Poverty Calculator")
    print("Connecting Schools and Donors to End Period Poverty")
    print("This application helps schools report the impact of period poverty on girls' education, and helps donors see where their support can make a measurable difference.")

def role_selection():
    print("What are you logging in as?")
    print("1. School")
    print("2. Donor")
    print("3. Exit")
    choice = input("Enter your choice(1-3):")
    return choice
if __name__ == "__main__":
    welcome_message()
    role = role_selection()
    print(f"You selected {role}")


import sqlite3
from datetime import date

DATABASE = "herperiod.db"
SQL_FILE = "schools_records.sql"

# ============================================================
#   MEMBER 2 — SCHOOL REGISTRATION
#   Functions: create_schools_table, get_school_data,
#              save_school_data, display_schools_table,
#              school_registration

def create_database():
    """Creates the database and schools table using schools.sql."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    with open(SQL_FILE, "r") as file:
        cursor.executescript(file.read())
>>>>>>> 9d1a037d960eaad647509789e7eed84f955ee553

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
=======
def get_school_data(school_name):
    """Retrieve school data if it already exists."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM schools WHERE school_name = ?",
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
    """Insert or update school information."""

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO schools
        (
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
    """Display every school currently stored."""

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
# MAIN PROGRAM
# ============================================================
REGISTERED_SCHOOLS = [
        "Kigali High School",
        "GS KIMIRONKO 1",
        "Ecole St Rita",
        "Green Hills Academy",
        ]


def school_registration():

    create_database()

    print("\n===============================")
    print(" SCHOOL REGISTRATION SYSTEM")
    print("===============================")

    school_name = input("\nEnter your school name: ").strip()
    if school_name not in REGISTERED_SCHOOLS:
        print(f"\nSorry, '{school_name}' is not on our list of registered schools.")
        print("Only registered schools may proceed. Please contact the program administrator if you believe this is an error.")
        return None                                              # <-- NEW 
    existing = get_school_data(school_name)

    if existing:

        print(f"\nWelcome back, {school_name}!")

        print("\nSchool information already exists.\n")

        print(f"Population: {existing[2]}")
        print(f"Girls Affected: {existing[3]}")
        print(f"Days Missed: {existing[4]}")
        print(f"Pad Cost: {existing[5]}")

        return {
            "school_name": existing[1],
            "population": existing[2],
            "girls_affected": existing[3],
            "days_missed": existing[4],
            "pad_cost": existing[5]
        }

    print(f"\nWelcome, {school_name}!")
    print("No information found.")
    print("Please register your school.\n")

    while True:

        try:

            population = int(
                input("Total student population: ")
            )

            girls_affected = int(
                input("Number of school-aged girls: ")
            )

            days_missed = float(
                input("Average school days missed annually: ")
            )

            pad_cost = float(
                input("Average price of ONE sanitary pad (RWF): ")
            )

            break

        except ValueError:

            print("\nPlease enter valid numbers.\n")

    
    

    
        
    
    



    save_school_data(
        school_name,
        population,
        girls_affected,
        days_missed,
        pad_cost,
        days_lost,
        annual_cost
    )
# ============================================================
    # SAVE CHANGES
    # ============================================================

    print("\n===============================")
    print(" SAVE CHANGES")
    print("===============================")

    while True:

        save_choice = input(
            "Would you like to save this information? (yes/no): "
        ).strip().lower()

        if save_choice == "yes":

            save_school_data(
                school_name,
                population,
                girls_affected,
                days_missed,
                pad_cost,
                days_lost,
                annual_cost
            )

            print("\n✓ Information saved successfully!")

            display_schools_table()

            break

        elif save_choice == "no":

            print("\nInformation was not saved.")

            break

        else:

            print("Please enter 'yes' or 'no'.")

    # ============================================================
    # EXIT SYSTEM
    # ============================================================

    print("\n===============================")
    print(" EXIT SYSTEM")
    print("===============================")

    while True:

        exit_choice = input(
            "Are you sure you want to exit? (yes/no): "
        ).strip().lower()

        if exit_choice == "yes":

            print("\nThank you for using the School Registration System.")
            print("Goodbye!")

            return {
                "school_name": school_name,
                "population": population,
                "girls_affected": girls_affected,
                "days_missed": days_missed,
                "pad_cost": pad_cost
            }

        elif exit_choice == "no":

            print("\nReturning to the registration system...\n")

            return school_registration()

        else:

            print("Please enter 'yes' or 'no'.")

    print("\nSchool successfully registered!")

    display_schools_table()

    return {
        "school_name": school_name,
        "population": population,
        "girls_affected": girls_affected,
        "days_missed": days_missed,
        "pad_cost": pad_cost
    }


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    school_registration()

>>>>>>> 9d1a037d960eaad647509789e7eed84f955ee553
