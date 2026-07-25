import sqlite3
from datetime import date

# ============================================================
#   MEMBER 2 — SCHOOL REGISTRATION
#   Functions: create_schools_table, get_school_data,
#              save_school_data, display_schools_table,
#              school_registration
# ============================================================

def create_schools_table():
    """Creates the schools table in the database if it doesn't exist."""
    conn = sqlite3.connect("herperiod.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schools (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            school_name    TEXT UNIQUE NOT NULL,
            population     INTEGER,
            girls_affected INTEGER,
            days_missed    REAL,
            pad_cost       REAL,
            days_lost      REAL,
            annual_cost    REAL,
            date_added     TEXT
        )
    """)
    conn.commit()
    conn.close()


def get_school_data(school_name):
    """Check if a school already exists in the database."""
    conn = sqlite3.connect("herperiod.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM schools WHERE school_name = ?", (school_name,)
    )
    result = cursor.fetchone()
    conn.close()
    return result


def save_school_data(school_name, population, girls_affected,
                     days_missed, pad_cost, days_lost, annual_cost):
    """Save a new school's data into the database."""
    conn = sqlite3.connect("herperiod.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO schools
        (school_name, population, girls_affected, days_missed,
         pad_cost, days_lost, annual_cost, date_added)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (school_name, population, girls_affected, days_missed,
          pad_cost, days_lost, annual_cost, str(date.today())))
    conn.commit()
    conn.close()


def display_schools_table():
    """Display all schools currently saved in the database."""
    conn = sqlite3.connect("herperiod.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM schools")
    rows = cursor.fetchall()
    conn.close()

    print("\nCurrent contents of the schools table:")
    print(f"\n{'School':<20} {'Population':<12} {'Girls Affected':<16} "
          f"{'Days Missed':<13} {'Pad Cost':<10} "
          f"{'Days Lost':<12} {'Annual Cost'}")
    print("-" * 110)
    for row in rows:
        print(f"{row[1]:<20} {row[2]:<12} {row[3]:<16} "
              f"{row[4]:<13} {row[5]:<10} "
              f"{row[6]:<12} {row[7]:.2f}")


def school_registration():
    """
    Main Member 2 function.
    Handles school registration and returns school data
    for Member 3 to use in calculations.
    """
    create_schools_table()

    print("\n[03] School Registration")
    print("    Question: Prompt the user to enter their school name...")
    print("-" * 70)

    school_name = input("\nEnter your school name: ").strip()

    existing = get_school_data(school_name)

    if existing:
        print(f"Access granted. Welcome back, {school_name}.")
        return {
            "school_name"   : existing[1],
            "population"    : existing[2],
            "girls_affected": existing[3],
            "days_missed"   : existing[4],
            "pad_cost"      : existing[5]
        }

    else:
        print(f"Access granted. Welcome, {school_name}.")
        print(f"\nNo data on file yet for {school_name}. Let's set that up.")

        while True:
            try:
                population     = int(input("Total number of students (population): "))
                girls_affected = int(input("Number of school-aged girls (menstruating age): "))
                days_missed    = float(input("Average school days missed per menstruating girl annually: "))
                pad_cost       = float(input("Average price of one sanitary pad (RWF): "))
                break
            except ValueError:
                print("Invalid input. Please enter numbers only.\n")

        pads_per_period = days_missed * 4
        pads_per_year   = pads_per_period * 12
        annual_cost     = pads_per_year * pad_cost * girls_affected
        days_lost       = girls_affected * days_missed * 12

        save_school_data(school_name, population, girls_affected,
                         days_missed, pad_cost, days_lost, annual_cost)

        print(f"\nData for {school_name} has been saved.")

        display_schools_table()

        return {
            "school_name"   : school_name,
            "population"    : population,
            "girls_affected": girls_affected,
            "days_missed"   : days_missed,
            "pad_cost"      : pad_cost
        }


# ── Temporary test runner (Member 1 will replace this) ──────
if __name__ == "__main__":
    school_registration()
=======
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

