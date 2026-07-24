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

