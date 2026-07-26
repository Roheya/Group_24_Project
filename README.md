**HerPeriod Poverty Calculator**

A command-line tool connecting schools and donors to help end period poverty — schools register impact data, and donors use that data to direct support where it's needed most.

**Overview**

The HerPeriod Poverty Calculator is a Python CLI application built around two user roles:

Schools register enrollment and period-poverty impact data (girls affected, school days missed, sanitary pad costs), and the system calculates the estimated annual cost and days lost.
Donors browse registered schools, view calculated impact, pledge donations, track their own donation history, and export a CSV report.

Data is persisted in a local SQLite database (herperiod.db).

**Project Structure**
Group_24_Project/
├── calculations.py            # Impact calculations (days lost, cost, severity, MissingDataError)
├── schools_records.sql        # SQL schema executed on first run to create the schools table
├── herperiod.db               # Created automatically on first run (SQLite database)
└── period.py                  # Created when a donor chooses to export a report

Note: calculations.py and schools_records.sql are required dependencies referenced by the main script but not shown in this excerpt — make sure both are present in the same directory before running.

**Requirements**
Python 3.8 or later
No external packages required — only the standard library (sqlite3, csv, datetime)

Check your Python version:

bash
python3 --version
**Setup**
Clone or download the project files into a single folder.
Confirm the following files are present together:
period.py
calculations.py
schools_records.sql
No manual database setup is needed — the app creates herperiod.db and the required tables automatically the first time it runs.
**Running the Application**

From inside the project folder, run:

bash
python3 period.py
Terminal walkthrough
$ python3 main.py

======================================================================
        HERPERIOD POVERTY CALCULATOR
======================================================================
Connecting Schools and Donors to End Period Poverty
This platform allows schools to register impact data and donors to
support schools in need.
Who Are You Logging In As?:
1. School
2. Donor
3. Exit
Enter your choice (1-3): 1

===============================
 SCHOOL REGISTRATION SYSTEM
===============================

Enter your school name: Excella High School

Welcome, Excella High School!
No school record found.
Please register your school.

Enter total student population: 450
Enter number of school-aged girls: 210
Average school days missed per year: 5
Cost of ONE sanitary pad (RWF): 500

===============================
 IMPACT SUMMARY
===============================
School Name      : Excella High School
Population       : 450
Girls Affected   : 210
Days Missed      : 5.0
Days Lost/Year   : 1050.0
Annual Pad Cost  : 105,000.00 RWF

Would you like to save this information? (yes/no): yes

✓ School information saved successfully!
Donor portal example
Who Are You Logging In As?:
1. School
2. Donor
3. Exit
Enter your choice (1-3): 2

==============================================================
                    DONOR PORTAL
==============================================================
Enter your name: Refilwe
Enter your pledge amount (RWF): 50000

Welcome Refilwe!

================ DONOR MENU ================
1. View Registered Schools
2. Donate to a School
3. View My Donations
4. Export Schools Report
5. Logout

Enter your choice (1-5): 2

Available Schools
1. Excella High School

Select a school: 1

Use your original pledge of 50,000.00 RWF? (yes/no): yes

✓ Donation recorded successfully!
Donor  : Refilwe
School : Excella High School
Amount : 50,000.00 RWF
IR-6. Recognized Schools

School registration is currently limited to a fixed allow-list of schools recognized by the Rwanda Public Basic Education system:

Excella High School
GS KIMIRONKO 1
GS KIMIRONKO 2
Ecole St Rita
Kigali High School
Green Hill Academy
GS Runda Isonga
GS Burema

Entering a school name outside this list returns a "not recognised" message and exits registration.

**Data Model**

schools table (created from schools_records.sql)

Column	Description
school_name	Unique school identifier (primary key expected)
population	Total student population
girls_affected	Number of school-aged girls
days_missed	Average school days missed per year
pad_cost	Cost of one sanitary pad (RWF)
days_lost	Calculated total days lost per year
annual_cost	Calculated total annual pad cost (RWF)
date_added	Date the record was created

pledges table (created at runtime)

Column	Description
id	Auto-incrementing primary key
donor_name	Name of the donor
school_name	School the pledge supports
pledge_amount	Pledge amount (RWF)
pledge_date	Timestamp of the pledge


**Known Limitations / Next Steps**
School allow-list is hardcoded; moving it to a config file or database table would make it easier to maintain.
No password/authentication layer — role selection is currently name-based only.
Project is being migrated from SQLite to MySQL as the underlying data store; this script reflects the SQLite version.
**Contributors**
Roheya - Welcome Message and Log-in Options
Elham - School Registration
Becky - Calculations
Pax - Pledge Application
Refilwe - Connection of Databases and Save and Listing Reporting & Logout

The code is organized into four member-owned sections (Welcome Screen, School Registration, Calculations, Donor Workflow) — update this table with who owned which section.
