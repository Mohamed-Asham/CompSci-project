import pandas as pd
import calendar
from datetime import datetime, timedelta, time


def generate_calendar(year, month):
    month_days = calendar.monthcalendar(year, month)
    calendar_df = pd.DataFrame(month_days, columns=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    calendar_df.replace(0, "", inplace=True)
    print(f"\nCalendar for {calendar.month_name[month]} {year}")
    print(calendar_df.to_string(index=False))


def create_daily_calendar(date):
    time_slots = [datetime.strptime(f"{hour}:{minute}", "%H:%M").time()
                  for hour in range(9, 17) for minute in (0, 30)]
    calendar_df = pd.DataFrame({"Time Slot": time_slots, "Appointment": "Available"})
    return calendar_df


def display_calendar(date):
    calendar_df = create_daily_calendar(date)
    print(f"\nCalendar for {date.strftime('%A, %d %B %Y')}")
    print(calendar_df.to_string(index=False))


def book_appointment(date, daily_calendar):
    print(f"\nBooking Calendar for {date.strftime('%A, %d %B %Y')}")
    print(daily_calendar.to_string(index=False))

    while True:
        try:
            time_input = input("Enter the time slot to book in HH:MM format (or type 'exit' to quit): ")
            if time_input.lower() == 'exit':
                print("Exiting booking system.")
                break

            # Convert input to time object
            time_slot = datetime.strptime(time_input, "%H:%M").time()

            # Attempt to book the slot
            if time_slot in daily_calendar["Time Slot"].values:
                if daily_calendar.loc[daily_calendar["Time Slot"] == time_slot, "Appointment"].values[0] == "Available":
                    daily_calendar.loc[daily_calendar["Time Slot"] == time_slot, "Appointment"] = "Booked"
                    print(f"Slot at {time_slot} has been successfully booked.")
                    print(f"\nUpdated Calendar for {date.strftime('%A, %d %B %Y')}")
                    print(daily_calendar.to_string(index=False))
                    break  # End after successfully booking one slot
                else:
                    print(f"Slot at {time_slot} is already booked. Please choose another time.")
            else:
                print(f"Invalid time slot: {time_slot}. Please choose a valid time.")
        except ValueError:
            print("Invalid time format. Please use HH:MM format.")

    print("Thank you for booking an appointment.")


def cancel_appointment(date, daily_calendar):
    print(f"\nCancellation Calendar for {date.strftime('%A, %d %B %Y')}")
    print(daily_calendar.to_string(index=False))

    while True:
        try:
            time_input = input("Enter the time slot to cancel in HH:MM format (or type 'exit' to quit): ")
            if time_input.lower() == 'exit':
                print("Exiting cancellation system.")
                break

            # Convert input to time object
            time_slot = datetime.strptime(time_input, "%H:%M").time()

            # Attempt to cancel the slot
            if time_slot in daily_calendar["Time Slot"].values:
                if daily_calendar.loc[daily_calendar["Time Slot"] == time_slot, "Appointment"].values[0] == "Booked":
                    daily_calendar.loc[daily_calendar["Time Slot"] == time_slot, "Appointment"] = "Available"
                    print(f"Slot at {time_slot} has been successfully canceled.")
                    print(f"\nUpdated Calendar for {date.strftime('%A, %d %B %Y')}")
                    print(daily_calendar.to_string(index=False))
                    break  # End after successfully canceling one slot
                else:
                    print(f"Slot at {time_slot} is not booked. Please choose another time.")
            else:
                print(f"Invalid time slot: {time_slot}. Please choose a valid time.")
        except ValueError:
            print("Invalid time format. Please use HH:MM format.")


# Main Program Usage
while True:
    try:
        MM, YYYY = input("Choose the Month and Year using MM YYYY format: ").split()
        mm = int(MM)
        if mm < 1 or mm > 12:
            print("Invalid month. Please enter a month between 01 and 12.")
            continue
        yyyy = int(YYYY)
        if yyyy < 2000 or yyyy > 2100:
            print("Invalid year. Please enter a year between 2000 and 2100.")
            continue
        break
    except ValueError:
        print("Invalid format. Please use MM YYYY format.")

print("------------------\n------------------")
generate_calendar(yyyy, mm)

print("------------------\n------------------")
while True:
    try:
        DD = input("Choose the date in DD format: ")
        dd = int(DD)
        if 1 <= dd <= 31:
            break
        else:
            print("Invalid day. Please enter a valid day for the selected month.")
    except ValueError:
        print("Invalid format. Please use DD format.")

print("------------------\n------------------")

selected_date = datetime(yyyy, mm, dd)
daily_calendar = create_daily_calendar(selected_date)

while True:
    display_calendar(selected_date)

    print("\nOptions: ")
    print("1. Book an appointment")
    print("2. Cancel an appointment")
    print("3. Exit")
    choice = input("Select an option: ")

    if choice == "1":
        book_appointment(selected_date, daily_calendar)
    elif choice == "2":
        cancel_appointment(selected_date, daily_calendar)
    elif choice == "3":
        print("Thank you for using the appointment system. Goodbye!")
        break
    else:
        print("Invalid option. Please choose 1, 2, or 3.")
