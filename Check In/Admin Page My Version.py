#======================Admin Homepage======================
def display_all_accounts():
    print("=" * 80)
    print("ALL ACCOUNTS".center(80))
    print("\nEnter 'H' to return to the homepage")

    if not registered_users:
        print("No accounts available.")
        return

    account_mapping = {}
    counter = 1

    for role, accounts in registered_users.items():
        print(f"\nRole: {role.capitalize()}")
        print("-" * 80)
        if accounts:
            for email, details in accounts.items():
                print(f"[ {counter} ] Email: {email}, Name: {details['name']}, "
                      f"Surname: {details['surname']}, Gender: {details['gender']}, "
                      f"Password: {details['password']}")
                account_mapping[counter] = (role, email)  # Map the number to role and email
                counter += 1
        else:
            print("No accounts in this role.")
    print(f"\n{"=" * 80}")

    return account_mapping
def delete_accounts():
    account_mapping = display_all_accounts()
    print("\nEnter 'H' to return to the homepage\n")

    while True:
        choice = input("Enter the number of the account to delete: ").strip()
        if choice.upper() == "H":
            admins_page()
            return

        try:
            account_numbers = [int(num.strip()) for num in choice.split(",")]
        except ValueError:
            print("Invalid input. Please enter numbers corresponding to accounts, separated by commas.")
            continue

        invalid_numbers = [num for num in account_numbers if num not in account_mapping]
        if invalid_numbers:
            print(f"Invalid numbers found: {', '.join(map(str, invalid_numbers))}")
            continue

        # Process valid account numbers
        for numbers in account_numbers:
            role, email_to_delete = account_mapping[numbers]
            confirming_option = input(
                f"Confirm deletion of account [ {numbers} ] [ {email_to_delete} ] (Y/N): ").strip().upper()
            if confirming_option == "Y":
                del registered_users[role][email_to_delete]
                save_accounts(registered_users, mode="override")
                print(f"\nAccount with email '{email_to_delete}' has been successfully deleted.")
                sleep(2)
                print("\nUpdated Accounts:")
                display_all_accounts()
            elif confirming_option == "N":
                print("Account deletion cancelled.")
            else:
                print("Invalid input. Please confirm with 'Y' or 'N'")

#other functions...
#==========================================================


def admins_page():
    print("=" * 80)
    print("ADMIN HOMEPAGE".center(80))
    print(termcolor.colored("Welcome, Admin. Managing the platform for better mental health!".center(80), "green"))
    print("-" * 80)
    print("[ 1 ] Add New MHWP")
    print("[ 2 ] Activate/Deactivate or Delete accounts ")
    print("[ 3 ] Change GP Details ")
    print("[ 4 ] Change Patient Details ")
    print("[ 5 ] Display User Details")
    print("[ X ] Logout")

    while True:
        choice = input("\nPlease select and option: ").strip()
        if choice.upper() == "X":
            login_menu()
        elif choice == "1":
            def manage_gp_system():
                import json
                from datetime import datetime

                # Path to the JSON file
                DATA_FILE = "data.json"

                # Load JSON data from file
                def load_data():
                    try:
                        with open(DATA_FILE, "r") as file:
                            return json.load(file)
                    except FileNotFoundError:
                        return {"patient": {}, "gp": {}, "admin": {}}

                # Save JSON data to file
                def save_data(data):
                    with open(DATA_FILE, "w") as file:
                        json.dump(data, file, indent=4)

                # Register a new GP
                def register_gp():
                    """Function to register a new General Practitioner (GP)."""
                    print("\nRegister a new GP:")
                    email = input("Email: ").strip()
                    password = input("Password: ").strip()
                    name = input("First Name: ").strip()
                    surname = input("Surname: ").strip()
                    date_of_birth = input("Date of Birth (DD/MM/YYYY): ").strip()
                    gender = input("Gender: ").strip()
                    NHS_blood_donor = input("NHS Blood Donor (Yes/No): ").strip()
                    NHS_organ_donor = input("NHS Organ Donor (Yes/No): ").strip()
                    address_line_1 = input("Address Line 1: ").strip()
                    address_line_2 = input("Address Line 2: ").strip()

                    data = load_data()

                    if email in data["gp"]:
                        print(f"\nError: GP with email {email} already exists.")
                        return

                    # Create a new GP entry
                    data["gp"][email] = {
                        "email": email,
                        "password": password,
                        "name": name,
                        "surname": surname,
                        "date_of_birth": date_of_birth,
                        "gender": gender,
                        "NHS_blood_donor": NHS_blood_donor,
                        "NHS_organ_donor": NHS_organ_donor,
                        "Address_Line_1": address_line_1,
                        "Address_Line_2": address_line_2,
                        "conditions": [],
                        "clinical_notes": "None",
                        "journals": []
                    }

                    save_data(data)
                    print(f"\n{name} {surname} has been successfully registered as a GP.")

                # Display all GPs
                def display_gps():
                    """Display all registered GPs."""
                    data = load_data()
                    gps = data.get("gp", {})

                    if not gps:
                        print("\nNo GPs registered yet.")
                        return

                    print("\nRegistered GPs:")
                    for i, (email, details) in enumerate(gps.items(), start=1):
                        print(f"{i}. {details['name']} {details['surname']} ({email})")

                # Main program loop
                while True:
                    print("\n[1] Register a new GP")
                    print("[2] View all GPs")
                    print("[X] Return To Admin Homepage")

                    choice = input("Enter your choice: ").strip()

                    if choice == '1':
                        register_gp()
                    elif choice == '2':
                        display_gps()
                    elif choice == '':
                        print("Exiting the program.")
                        break
                    else:
                        print("Invalid choice. Please try again.")

            if __name__ == "__main__":
                manage_gp_system()

            main_menu()
        elif choice == "2":
            delete_accounts()
        elif choice == "3":
            def manage_gp_details():
                from time import sleep

                # GP data
                gp_data = {
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

                # Function to display all GPs with name and email
                def display_all_gps():
                    if not gp_data:
                        print("No GPs found.")
                        return {}

                    print("List of GPs:\n")
                    for index, (email, details) in enumerate(gp_data.items(), start=1):
                        print(f"[{index}] Name: {details['name']} {details['surname']}, Email: {email}")

                    return {i + 1: (email, details) for i, (email, details) in enumerate(gp_data.items())}

                # Function to update GP details
                def update_gp_details(email_to_edit):
                    gp_details = gp_data[email_to_edit]

                    # Display the current GP details before editing
                    print("\nCurrent GP Details:")
                    print(f"[1] Email: {gp_details['email']}")
                    print(f"[2] Password: {gp_details['password']}")
                    print(f"[3] Name: {gp_details['name']}")
                    print(f"[4] Surname: {gp_details['surname']}")
                    print(f"[5] Date of Birth: {gp_details['date_of_birth']}")
                    print(f"[6] Gender: {gp_details['gender']}")
                    print(f"[7] NHS Blood Donor: {gp_details['NHS_blood_donor']}")
                    print(f"[8] NHS Organ Donor: {gp_details['NHS_organ_donor']}")
                    print(f"[9] Address Line 1: {gp_details['Address_Line_1']}")
                    print(f"[10] Address Line 2: {gp_details['Address_Line_2']}")

                    print("\nWhich detail would you like to edit?")

                    choice = input("Enter your choice: ").strip().upper()

                    if choice == "H":
                        print("Returning to the homepage...\n")
                        return

                    if choice == "1":
                        new_email = input(f"Enter new Email (current: {gp_details['email']}): ").strip()
                        gp_details["email"] = new_email

                    elif choice == "2":
                        new_password = input(f"Enter new Password (current: {gp_details['password']}): ").strip()
                        gp_details["password"] = new_password

                    elif choice == "3":
                        new_name = input(f"Enter new Name (current: {gp_details['name']}): ").strip()
                        gp_details["name"] = new_name

                    elif choice == "4":
                        new_surname = input(f"Enter new Surname (current: {gp_details['surname']}): ").strip()
                        gp_details["surname"] = new_surname

                    elif choice == "5":
                        new_dob = input(f"Enter new Date of Birth (current: {gp_details['date_of_birth']}): ").strip()
                        gp_details["date_of_birth"] = new_dob

                    elif choice == "6":
                        new_gender = input(f"Enter new Gender (current: {gp_details['gender']}): ").strip()
                        gp_details["gender"] = new_gender

                    elif choice == "7":
                        new_blood_donor = input(
                            f"Enter new NHS Blood Donor status (current: {gp_details['NHS_blood_donor']}): ").strip()
                        gp_details["NHS_blood_donor"] = new_blood_donor

                    elif choice == "8":
                        new_organ_donor = input(
                            f"Enter new NHS Organ Donor status (current: {gp_details['NHS_organ_donor']}): ").strip()
                        gp_details["NHS_organ_donor"] = new_organ_donor

                    elif choice == "9":
                        new_address_line_1 = input(
                            f"Enter new Address Line 1 (current: {gp_details['Address_Line_1']}): ").strip()
                        gp_details["Address_Line_1"] = new_address_line_1

                    elif choice == "10":
                        new_address_line_2 = input(
                            f"Enter new Address Line 2 (current: {gp_details['Address_Line_2']}): ").strip()
                        gp_details["Address_Line_2"] = new_address_line_2

                    else:
                        print("Invalid option. Returning to the homepage...\n")
                        return

                    print("\nUpdated GP Details:")
                    for key, value in gp_details.items():
                        print(f"{key.replace('_', ' ').title()}: {value}")

                    print("\nChanges saved successfully!")

                # Function to display options and allow selection of a GP to edit
                while True:
                    print("\n[1] Display and Edit GP Details")
                    print("[H] Return to Homepage")

                    option = input("Enter your choice: ").strip().upper()

                    if option == "1":
                        account_mapping = display_all_gps()
                        if account_mapping:
                            try:
                                choice = int(input("Enter the number of the GP to edit: ").strip())
                                email_to_edit = account_mapping[choice][0]
                                update_gp_details(email_to_edit)
                            except (ValueError, KeyError):
                                print("Invalid option. Please try again.")
                    elif option == "H":
                        print("Returning to the homepage...\n")
                        break
                    else:
                        print("Invalid option. Please try again.")

            # Call the function
            manage_gp_details()

            print("FUNCTION NOT ADDED. WORK IN PROGRESS")  # <---------------------------Put function here.
            main_menu()
        elif choice == "4":
            # Function to load accounts (placeholder)
            def load_accounts():
                import json
                try:
                    with open("accounts.json", "r") as file:
                        return json.load(file)
                except FileNotFoundError:
                    return {"patient": {}, "gp": {}, "admin": {}}

            # Placeholder function for patients_page
            def patients_page(email_address):
                print(f"Returning to the patient's homepage for {email_address}.")

            # Function to update account details
            def update_account_page(email_address):
                from time import sleep
                from datetime import datetime
                import re
                from random import randint
                from json import dump

                def match(pattern, string):
                    return re.match(pattern, string)

                data = load_accounts()
                account_details = data["patient"][email_address]
                updates_made = False

                while True:
                    print("=" * 80)
                    print("Account Details:\n".center(80))
                    counter = 1
                    for key, value in account_details.items():
                        if key not in {"password", "journals", "conditions", "clinical_notes"}:
                            print(f"[{counter}] {key[0].upper() + key[1:].replace('_', ' ')}: {value}")
                            counter += 1
                    print("\n[ H ]  Go to Homepage\n")

                    update_option = input("Please select an option to edit: ").strip()

                    if update_option.upper() == "H":
                        print("Returning to your homepage...\n")
                        sleep(1)
                        patients_page(email_address)
                        break

                    if update_option.isdigit() and 0 < int(update_option) <= counter:
                        update_option = int(update_option)
                    else:
                        print("\nInvalid input. Please choose a valid option.")
                        continue

                    # Example of updating first name (extend for other fields as needed)
                    if update_option == 2:  # Assuming 2 corresponds to "First Name"
                        new_first_name = input("Please enter your new first name: ").strip()
                        if new_first_name != account_details["name"]:
                            while True:
                                final_confirmation = input(
                                    "Please confirm you would like to make this change to your account (Y/N): "
                                ).strip().lower()
                                if final_confirmation == "y":
                                    account_details["name"] = new_first_name
                                    updates_made = True
                                    break
                                elif final_confirmation == "n":
                                    break
                                else:
                                    print("Please input a valid option, either Y or N.")

                        else:
                            print("This is already your current first name.")

                    # Save changes if any updates were made
                    if updates_made:
                        data["patient"][email_address] = account_details
                        with open("accounts.json", "w") as file:
                            dump(data, file, indent=4)
                        print("Updating your account details...")
                        sleep(1)
                        print("Your changes have been saved successfully!")
                        sleep(1)
                        updates_made = False

                    edit_again = input("Would you like to edit another detail? (Y/N): ").strip().lower()
                    if edit_again == "n":
                        print("\nReturning to your homepage...")
                        sleep(1)
                        patients_page(email_address)
                        break

            # Main menu function
            def main_menu():
                while True:
                    print("\nMain Menu:")
                    print("[1] Option 1")
                    print("[2] Option 2")
                    print("[3] Option 3")
                    print("[4] Update Account Page")
                    print("[5] Exit")

                    choice = input("Enter your choice: ").strip()

                    if choice == "4":
                        email_address = input("Enter your email address to update account: ").strip()
                        update_account_page(email_address)  # Call the function here
                    elif choice == "5":
                        print("Exiting the program. Goodbye!")
                        break
                    else:
                        print("Invalid choice. Please try again.")

            # Run the main menu
            main_menu()

            print("FUNCTION NOT ADDED. WORK IN PROGRESS")  # <---------------------------Put function here.
            main_menu()
        elif choice == "5":
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
            print("FUNCTION NOT ADDED. WORK IN PROGRESS")  # <---------------------------Put function here.
            main_menu()
        else:
            print("Please choose a valid option '1' , '2', '3', '4', '5' or 'X'")
# ==========================================================

admins_page()