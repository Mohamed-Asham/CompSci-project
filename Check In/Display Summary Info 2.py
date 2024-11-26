def display_summary_info_system():
    """
    Displays a summary system for viewing patient and MHWP details,
    along with their appointments or bookings.
    """
    # Embedded JSON data as a Python dictionary
    json_data = {
        "patient": {
            "mnedjadi2003@gmail.com": {
                "email": "mnedjadi2003@gmail.com",
                "password": "Yamina20",
                "name": "mohamed",
                "surname": "nedjadi",
                "date_of_birth": "05/11/2003",
                "gender": "Male",
                "NHS_blood_donor": "IS Blood donor",
                "NHS_organ_donor": "IS Organ donor",
                "Address_Line_1": "401 Jutsum",
                "Address_Line_2": "lONNDON",
                "journals": [
                    {
                        "date": "2024-11-24 15:47:03",
                        "entry": "cwdhcfwefhciwehfwef\nwefuiweifherwighfer\newfuiwehfopwehfwe["
                    }
                ],
                "conditions": [],
                "clinical_notes": "None"
            },
            "tangid.mhm03@outlook.com": {
                "email": "tangid.mhm03@outlook.com",
                "password": "Excalibur5",
                "name": "Tangid",
                "surname": "Mohammad",
                "date_of_birth": "16/09/2003",
                "gender": "Male",
                "NHS_blood_donor": "IS Blood donor",
                "NHS_organ_donor": "NOT Organ donor",
                "Address_Line_1": "86 Victoria Road",
                "Address_Line_2": "London",
                "journals": [
                    {
                        "date": "2024-11-24 16:49:05",
                        "entry": "Hello, my name is Tangid\nI want to go home\n\n\nBye"
                    }
                ],
                "conditions": [],
                "clinical_notes": "None"
            }
        },
        "gp": {  # Treating 'gp' as MHWPs
            "gp1@gmail.com": {
                "email": "gp1@gmail.com",
                "password": "password1",
                "name": "Unknown",
                "surname": "Unknown",
                "date_of_birth": "Unknown",
                "gender": "Unknown",
                "NHS_blood_donor": "Unknown",
                "NHS_organ_donor": "Unknown",
                "Address_Line_1": "Unknown",
                "Address_Line_2": "Unknown",
                "conditions": [],
                "clinical_notes": "None",
                "journals": []
            }
        }
    }

    # Sample bookings
    bookings = [
        {"patient": "mohamed nedjadi", "mhwp": "Unknown Unknown", "date": "2024-11-25"},
        {"patient": "Tangid Mohammad", "mhwp": "Unknown Unknown", "date": "2024-11-26"},
        {"patient": "mohamed nedjadi", "mhwp": "Unknown Unknown", "date": "2024-11-27"},
    ]

    # Combine patients and MHWPs into a single dictionary
    users = {
        **json_data["patient"],
        **json_data["gp"],  # Add GPs as MHWPs
    }

    def list_users():
        """Display all users and allow the user to select one to view details."""
        while True:  # Keep the menu accessible
            user_list = list(users.items())
            print("\nList of Users:")
            for idx, (email, data) in enumerate(user_list, 1):
                user_type = "Patient" if email in json_data["patient"] else "MHWP"
                full_name = f"{data['name']} {data['surname']}"
                print(f"[{idx}] {full_name} ({user_type})")

            print("[0] Exit")

            # Select a user
            while True:
                try:
                    choice = int(input("\nSelect a user to view details (or 0 to exit): "))
                    if choice == 0:
                        print("Press 0 again to exit or return to the menu.")
                        return  # Exits the function but keeps the menu accessible
                    elif 1 <= choice <= len(user_list):
                        email, data = user_list[choice - 1]
                        view_user_details(email, data)
                        break  # Return to the menu after viewing details
                    else:
                        print("Invalid choice. Please choose a valid option.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

    def view_user_details(email, data):
        """View detailed information about the selected user."""
        full_name = f"{data['name']} {data['surname']}"
        user_type = "Patient" if email in json_data["patient"] else "MHWP"
        print(f"\nDetails for {full_name}:")
        print(f"Email: {email}")
        print(f"Date of Birth: {data['date_of_birth']}")
        print(f"Gender: {data['gender']}")
        print(f"NHS Blood Donor: {data['NHS_blood_donor']}")
        print(f"NHS Organ Donor: {data['NHS_organ_donor']}")
        print(f"Address: {data['Address_Line_1']}, {data['Address_Line_2']}")
        print(f"User Type: {user_type}")

        if user_type == "Patient":
            # List appointments for the patient
            patient_bookings = [b for b in bookings if b["patient"].lower() == full_name.lower()]
            print(f"\nNumber of Appointments: {len(patient_bookings)}")
            for booking in patient_bookings:
                print(f"- Date: {booking['date']}, MHWP: {booking['mhwp']}")
        elif user_type == "MHWP":
            # List bookings for the MHWP
            mhwp_bookings = [b for b in bookings if b["mhwp"].lower() == full_name.lower()]
            print(f"\nNumber of Upcoming Bookings This Week: {len(mhwp_bookings)}")
            for booking in mhwp_bookings:
                print(f"- Date: {booking['date']}, Patient: {booking['patient']}")

        print("\nPress 0 to return to 'List Of Users'. ")
        input()  # Wait for user input to return to the main menu

    # Start the program
    list_users()


# Run the function
display_summary_info_system()

