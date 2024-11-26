#DISPLAY SUMMARY INFO
#DISPLAY SUMMARY INFO

import datetime


class User:
    def __init__(self, email, password, name, surname, date_of_birth, gender, NHS_blood_donor, NHS_organ_donor, address_line_1, address_line_2, user_type):
        self.email = email
        self.password = password
        self.name = name
        self.surname = surname
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.NHS_blood_donor = NHS_blood_donor  # "Yes" or "No"
        self.NHS_organ_donor = NHS_organ_donor  # "Yes" or "No"
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.user_type = user_type.lower()  # "patient" or "mhwp"
        self.is_disabled = False

    def full_name(self):
        """Return the full name of the user."""
        return f"{self.name} {self.surname}"

    def disable_user(self):
        """Disable the user."""
        self.is_disabled = True
        print(f"{self.full_name()} has been disabled.")

    def enable_user(self):
        """Enable the user."""
        self.is_disabled = False
        print(f"{self.full_name()} has been enabled.")


# Sample bookings system
bookings = [
    {"patient": "Alice Smith", "mhwp": "John Mike", "date": "2024-11-25"},
    {"patient": "Adam Scott", "mhwp": "John Mike", "date": "2024-11-26"},
    {"patient": "Alice Smith", "mhwp": "Julie Mitchell", "date": "2024-11-27"},
    {"patient": "Adam Scott", "mhwp": "Julie Mitchell", "date": "2024-11-28"},
    {"patient": "Alice Smith", "mhwp": "John Mike", "date": "2024-11-29"},
]

#Display The Details Of A Selected User
def view_user_details(user):
    user_name = user.full_name()
    current_date = datetime.date.today()
    current_week = current_date.isocalendar()[1]

    # Display user details
    print(f"\nDetails for {user_name}:")
    print(f"Email: {user.email}")
    print(f"Date of Birth: {user.date_of_birth}")
    print(f"Gender: {user.gender}")
    print(f"NHS Blood Donor: {user.NHS_blood_donor}")
    print(f"NHS Organ Donor: {user.NHS_organ_donor}")
    print(f"Address: {user.address_line_1}, {user.address_line_2}")
    print(f"User Type: {user.user_type.capitalize()}")
    print(f"Account Status: {'Disabled' if user.is_disabled else 'Active'}")

    if user.user_type == "mhwp":
        # MHWP: List upcoming bookings for the current week
        mhwp_bookings = [booking for booking in bookings if booking["mhwp"] == user_name]
        weekly_count = sum(
            datetime.date.fromisoformat(booking["date"]).isocalendar()[1] == current_week
            for booking in mhwp_bookings
        )
        print(f"\n{user_name} has {weekly_count} upcoming bookings this week:")
        for booking in mhwp_bookings:
            print(f"- Patient: {booking['patient']}, Date: {booking['date']}")

    elif user.user_type == "patient":
        # Patient: Total appointments and list of upcoming bookings
        patient_bookings = [booking for booking in bookings if booking["patient"] == user_name]
        upcoming_bookings = [
            booking for booking in patient_bookings
            if datetime.date.fromisoformat(booking["date"]) >= current_date
        ]
        print(f"\n{user_name} has {len(upcoming_bookings)} upcoming appointments:")
        for booking in upcoming_bookings:
            print(f"- MHWP: {booking['mhwp']}, Date: {booking['date']}")

    else:
        print("\nNo additional information available for this user type.")

#Display a list of all users and allow selection to view details.
def display_user_list(users):
    while True:
        print("\nUsers List:")
        for idx, user in enumerate(users, start=1):
            print(f"[{idx}] {user.full_name()} - {user.user_type.upper()}")

        print("[0] Exit")

        try:
            choice = int(input("\nSelect a user to view details (or 0 to exit): "))
            if choice == 0:
                print("Exiting user details view.")
                break
            elif 1 <= choice <= len(users):
                selected_user = users[choice - 1]
                view_user_details(selected_user)
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


# Example Users
users = [
    User("john.mike@example.com", "password123", "John", "Mike", "01/01/1980", "male", "Yes", "No", "123 Street", "Apt 1", "MHWP"),
    User("julie.mitchell@example.com", "password123", "Julie", "Mitchell", "15/03/1990", "female", "No", "Yes", "456 Road", "Apt 2", "MHWP"),
    User("alice.smith@example.com", "password123", "Alice", "Smith", "10/10/1985", "female", "Yes", "No", "789 Avenue", "Apt 3", "Patient"),
    User("adam.scott@example.com", "password123", "Adam", "Scott", "20/06/1975", "male", "No", "Yes", "101 Blvd", "Apt 4", "Patient"),
]

# Run the user display system
display_user_list(users)
