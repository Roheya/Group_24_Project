#!/usr/bin/python3
"""
Period Poverty Advocacy Platform

Integrated System

Member 1 - Welcome Screen
Member 2 - School Registration
Member 3 - Calculations
Member 4 - Donor Workflow
"""

import sqlite3
import csv
from datetime import date

import calculations
from calculations import MissingDataError

DATABASE = "herperiod.db"
SQL_FILE = "schools_records.sql"

# ============================================================
# MEMBER 1 - WELCOME SCREEN
# ============================================================

def welcome_message():
    """Display the application welcome message."""

    print("\n" + "=" * 70)
    print("        PERIOD POVERTY ADVOCACY PLATFORM")
    print("=" * 70)
    print("Connecting Schools and Donors to End Period Poverty")
    print(
        "This platform allows schools to register impact data "
        "and donors to support schools in need."
    )


def role_selection():
    """Display login menu."""

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
    Creates all required database tables.

    Reads the schools table from schools_records.sql
    and creates the donor pledges table.
    """

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create the schools table
    with open(SQL_FILE, "r") as file:
        cursor.executescript(file.read())

    # Create donor pledges table
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
    """Retrieve school information if it exists."""

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

    school = cursor.fetchone()

    conn.close()

    return school


def save_school_data(
        school_name,
        population,
        girls_affected,
        days_missed,
        pad_cost,
        days_lost,
        annual_cost):
    """Save or update school information."""

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
    """Display all registered schools."""

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
    """Return all registered schools."""

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
    """Save a donor pledge."""

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
# MEMBER 2 - SCHOOL REGISTRATION
# ============================================================

def school_registration():
    """Register a new school or retrieve an existing one."""

    create_database()

    print("\n===============================")
    print(" SCHOOL REGISTRATION SYSTEM")
    print("===============================")

    school_name = input("\nEnter your school name: ").strip()

    # List of schools recognized by the Rwanda Public Basic Education
    recognized_schools = [
        "Excella High School",
        "GS KIMIRONKO 1",
        "GS KIMIRONKO 2",
        "Ecole St Rita",
        "Kigali High School",
        "Green Hill Academy",
        "GS Runda Isonga",
        "GS Burema"
    ]

    if school_name not in recognized_schools:
        print("\nThe school is not recognised by the Rwanda Public Basic Education.")
        return

    existing = get_school_data(school_name)

    # --------------------------------------------------------
    # EXISTING SCHOOL
    # --------------------------------------------------------

    if existing:

        print(f"\nWelcome back, {school_name}!")

        print("\nSchool information already exists.")

        print(f"Population      : {existing[2]}")
        print(f"Girls Affected  : {existing[3]}")
        print(f"Days Missed     : {existing[4]}")
        print(f"Pad Cost        : {existing[5]} RWF")
        print(f"Days Lost       : {existing[6]}")
        print(f"Annual Cost     : {existing[7]:,.2f} RWF")

        input("\nPress Enter to return to the Main Menu...")
        return

    # --------------------------------------------------------
    # NEW SCHOOL REGISTRATION
    # --------------------------------------------------------

    print(f"\nWelcome, {school_name}!")
    print("No school record found.")
    print("Please register your school.\n")

    while True:

        try:

            population = int(
                input("Enter total student population: ")
            )

            girls_affected = int(
                input("Enter number of school-aged girls: ")
            )

            days_missed = float(
                input("Average school days missed per year: ")
            )

            pad_cost = float(
                input("Cost of ONE sanitary pad (RWF): ")
            )

            break

        except ValueError:

            print("\nPlease enter valid numeric values.\n")

    # --------------------------------------------------------
    # MEMBER 3: CALCULATIONS
    # --------------------------------------------------------

    try:
        days_lost = calculations.days_lost(girls_affected, days_missed)
        annual_cost = calculations.estimated_cost(girls_affected, pad_cost)
        girls_affected = calculations.girls_affected(girls_affected)
        severity = calculations.severity_score(days_missed)

    except MissingDataError as error:
        print(f"\nError: {error}")
        print("Registration cancelled. Please try again.")
        return

    # --------------------------------------------------------
    # DISPLAY CALCULATED RESULTS
    # --------------------------------------------------------

    print("\n===============================")
    print(" IMPACT SUMMARY")
    print("===============================")

    print(f"School Name      : {school_name}")
    print(f"Population       : {population}")
    print(f"Girls Affected   : {girls_affected}")
    print(f"Days Missed      : {days_missed}")
    print(f"Days Lost/Year   : {days_lost}")
    print(f"Annual Pad Cost  : {annual_cost:,.2f} RWF")

    # --------------------------------------------------------
    # SAVE DATA
    # --------------------------------------------------------

    while True:

        save = input(
            "\nWould you like to save this information? (yes/no): "
        ).strip().lower()

        if save in ["yes", "y"]:

            save_school_data(
                school_name,
                population,
                girls_affected,
                days_missed,
                pad_cost,
                days_lost,
                annual_cost
            )

            print("\n✓ School information saved successfully!")

            display_schools_table()

            break

        elif save in ["no", "n"]:

            print("\nRegistration cancelled.")
            return

        else:

            print("Please enter yes or no.")

    # --------------------------------------------------------
    # EXIT TO MAIN MENU
    # --------------------------------------------------------

    while True:

        choice = input(
            "\nReturn to the Main Menu? (yes/no): "
        ).strip().lower()

        if choice in ["yes", "y"]:

            print("\nReturning to Main Menu...\n")
            return

        elif choice in ["no", "n"]:

            print("\nCurrent School Summary\n")

            print(f"School Name      : {school_name}")
            print(f"Population       : {population}")
            print(f"Girls Affected   : {girls_affected}")
            print(f"Days Missed      : {days_missed}")
            print(f"Pad Cost         : {pad_cost:,.2f} RWF")
            print(f"Days Lost        : {days_lost}")
            print(f"Annual Cost      : {annual_cost:,.2f} RWF")

        else:

            print("Please enter yes or no.")
# ============================================================
# MEMBER 4 - DONOR WORKFLOW
# ============================================================

def view_all_schools_impact():
    """Display all registered schools and their impact."""

    schools = get_all_schools()

    if not schools:
        print("\nNo registered schools found.")
        return

    print("\n==============================================================")
    print("               REGISTERED SCHOOLS")
    print("==============================================================")

    for school in schools:

        name, population, girls, missed, pad, lost, cost = school

        print(f"\nSchool Name        : {name}")
        print(f"Population         : {population}")
        print(f"Girls Affected     : {girls}")
        print(f"Days Missed        : {missed}")
        print(f"Days Lost          : {lost}")
        print(f"Annual Cost        : {cost:,.2f} RWF")


def pledge_to_school(donor_name, default_amount):
    """Allow donors to donate to a selected school."""

    schools = get_all_schools()

    if not schools:
        print("\nNo schools available.")
        return

    print("\nAvailable Schools")

    for i, school in enumerate(schools, start=1):
        print(f"{i}. {school[0]}")

    try:

        choice = int(input("\nSelect a school: "))

        if choice < 1 or choice > len(schools):
            print("Invalid school selection.")
            return

        selected_school = schools[choice - 1][0]

        answer = input(
            f"\nUse your original pledge of "
            f"{default_amount:,.2f} RWF? (yes/no): "
        ).strip().lower()

        if answer in ["yes", "y"]:

            amount = default_amount

        else:

            amount = float(
                input("Enter new pledge amount (RWF): ")
            )

        record_pledge(
            donor_name,
            selected_school,
            amount
        )

        print("\n✓ Donation recorded successfully!")

        print(f"Donor  : {donor_name}")
        print(f"School : {selected_school}")
        print(f"Amount : {amount:,.2f} RWF")

    except ValueError:

        print("\nInvalid input.")


def view_my_donations(donor_name):
    """Display all donations made by the current donor."""

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            school_name,
            pledge_amount,
            pledge_date

        FROM pledges

        WHERE donor_name = ?

    """, (donor_name,))

    donations = cursor.fetchall()

    conn.close()

    if not donations:

        print("\nYou have not made any donations yet.")

        return

    print("\n==============================================================")
    print("                 MY DONATIONS")
    print("==============================================================")

    for donation in donations:

        print(f"\nSchool : {donation[0]}")
        print(f"Amount : {donation[1]:,.2f} RWF")
        print(f"Date   : {donation[2]}")


def list_and_export_report():
    """Display schools and export report to CSV."""

    schools = get_all_schools()

    if not schools:

        print("\nNo schools found.")

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

    if export in ["yes", "y"]:

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

            writer.writerows(schools)

        print(f"\n✓ Report exported successfully as '{filename}'.")


def donor_workflow():
    """Main donor menu."""

    print("\n==============================================================")
    print("                    DONOR PORTAL")
    print("==============================================================")

    donor_name = input("Enter your name: ").strip()

    try:

        pledge_amount = float(
            input("Enter your pledge amount (RWF): ")
        )

    except ValueError:

        pledge_amount = 0.0

    print(
        f"\nWelcome {donor_name}!"
    )

    while True:

        print("\n================ DONOR MENU ================")
        print("1. View Registered Schools")
        print("2. Donate to a School")
        print("3. View My Donations")
        print("4. Export Schools Report")
        print("5. Logout")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":

            view_all_schools_impact()

        elif choice == "2":

            pledge_to_school(
                donor_name,
                pledge_amount
            )

        elif choice == "3":

            view_my_donations(
                donor_name
            )

        elif choice == "4":

            list_and_export_report()

        elif choice == "5":

            print("\nLogging out...")

            break

        else:

            print("\nInvalid option.")
# ============================================================
# MAIN MENU
# ============================================================

def main():
    """Main application menu."""

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

            print("\n======================================")
            print(" Thank you for using the")
            print(" Period Poverty Advocacy Platform")
            print(" Goodbye!")
            print("======================================\n")

            break

        else:

            print("\nInvalid choice.")
            print("Please enter 1, 2 or 3.\n")


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()
