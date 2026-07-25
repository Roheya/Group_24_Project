#!/usr/bin/python3
def welcome_message():
    print("PERIOD POVERTY ADVOCACY PLATFORM")
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

    conn.commit()
    conn.close()


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

def school_registration():

    create_database()

    print("\n===============================")
    print(" SCHOOL REGISTRATION SYSTEM")
    print("===============================")

    school_name = input("\nEnter your school name: ").strip()

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

    # Calculations

    pads_per_period = days_missed * 4
    pads_per_year = pads_per_period * 12

    annual_cost = (
        pads_per_year *
        pad_cost *
        girls_affected
    )

    days_lost = (
        girls_affected *
        days_missed *
        12
    )

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

