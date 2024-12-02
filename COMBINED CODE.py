#=======================Modules=============================
from importlib import import_module
from time import sleep
from sys import exit, executable
from re import match
from random import randint
from datetime import datetime, timedelta, date
from json import load, dump, JSONDecodeError
from platform import system
import os
import subprocess
import sqlite3

# Must run to work with SQLite
sqlite3.register_adapter(date, lambda d: d.isoformat())
sqlite3.register_adapter(datetime, lambda d: d.isoformat())
sqlite3.register_converter("DATE", lambda s: datetime.strptime(s.decode(), "%Y-%m-%d").date())
sqlite3.register_converter("DATETIME", lambda s: datetime.strptime(s.decode(), "%Y-%m-%dT%H:%M:%S"))
# List of required non-standard packages
required_packages = ["pyfiglet", "termcolor", "pandas", "tabulate"]
def ensure_pip_installed():
    current_os = system()
    try:
        if current_os == "Windows":
            command = ["py", "-m", "pip", "--version"]
        else:
            command = [executable, "-m", "pip", "--version"]
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        # print("Pip is already installed.")


    except subprocess.CalledProcessError:
        print("Pip is not installed. Installing pip...")
        try:
            if current_os == "Windows":
                install_command = ["py", "-m", "pip", "install", "pip"]
            else:
                install_command = [executable, "-m", "ensurepip", "--upgrade"]
            subprocess.run(install_command, check=True)
            print("Pip installed successfully.")

        except subprocess.CalledProcessError as e:
            print(f"Failed to install pip: {e}")
            exit(1)
def install_modules():
    def install_and_import(package):
        try:
            __import__(package)
            # print(f"'{package}' is already installed.")
        except ImportError:
            print(f"'{package}' not installed. Installing...")

            current_os = system()

            if current_os == "Windows":
                # Command for Windows
                process = subprocess.run(f'cmd /c "py -m pip install {package}"',
                    shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            elif current_os == "Darwin":
                # Command for macOS
                process = subprocess.run(f'python3 -m pip install {package}',
                    shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            else:
                # For other Unix-like systems
                process = subprocess.run(f'python3 -m pip install {package}',
                    shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            #--------------OPTIONAL Prints the installation process output or errors ----------
            # print("Standard Output:")
            # print(process.stdout)
            # print("Standard Error (if any):")
            # print(process.stderr)
            #---------------------------------------------------------------------------------
            if process.returncode != 0:
                print(f"Error installing '{package}'. Exiting.")
                exit(1)
            else:
                # print(f"Successfully installed '{package}'.")
                pass

        globals()[package] = import_module(package)

    for packageS in required_packages:
        install_and_import(packageS)
def uninstall_modules():
    for package in required_packages:
        print(f"Uninstalling '{package}'...")
        current_os = system()
        if current_os == "Windows":
            process = subprocess.run(f'cmd /c "py -m pip uninstall {package}"',
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        else:
            process = subprocess.run(f'{executable} -m pip uninstall {package}',
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if process.returncode == 0:
            print(f"Successfully uninstalled '{package}'.")
        else:
            print(f"Error uninstalling '{package}':")
            print(process.stderr)
#==========================================================


#====================Header Display========================
def header():
    fig = pyfiglet.Figlet(font="dos_rebel", width=80, justify="center")  # List of optional fonts: big_money-ne, big_money-nw, ansi_regular
    title_art = fig.renderText("Breeeze")
    tagline = "Empowering your mental health journey"

    title_art_lines = title_art.splitlines()

    start = 0
    end = len(title_art_lines) - 1
    while end >= start and not title_art_lines[end].strip():
        end -= 1
    title_art_no_padding = "\n".join(title_art_lines[start:end + 1])

    # Calculate padding for the tagline
    line_width = 80  # Fixed width (adjustable)
    tagline_length = len(tagline)
    side_padding = (line_width - tagline_length - 4) // 2  # Subtracting 4 for "--" on each side
    left_padding = "~" * side_padding
    right_padding = "~" * (line_width - tagline_length - side_padding - 4)
    welcome_message = f"{left_padding} {tagline} {right_padding}"

    print("=" * line_width)
    print(termcolor.colored(title_art_no_padding, "cyan"))     #If you want to change color change here.
    print("=" * line_width)
    print(termcolor.colored(welcome_message, "yellow"))        #If you want to change color change here.
    print(f"{"=" * line_width}\n")
# =========================================================


#======================Database============================
DATA_FILE = "accounts.json"
def load_accounts():
    try:
        with open(DATA_FILE, "r") as file:
            data = load(file)

        if "admin" not in data:
            data["admin"] = {}
        if "gp" not in data:
            data["gp"] = {}
        if "patient" not in data:
            data["patient"] = {}

        for role, accounts in data.items():
            for email, details in accounts.items():
                # Only overwrite if the details are missing or incomplete
                if isinstance(details, dict):
                    # Ensure all keys exist, but keep existing values
                    details.setdefault("email", email)
                    details.setdefault("password", "Unknown")
                    details.setdefault("name", "Unknown")
                    details.setdefault("surname", "Unknown")
                    details.setdefault("date_of_birth", "Unknown")
                    details.setdefault("gender", "Unknown")
                    details.setdefault("NHS_blood_donor", "Unknown")
                    details.setdefault("NHS_organ_donor", "Unknown")
                    details.setdefault("Address_Line_1", "Unknown")
                    details.setdefault("Address_Line_2", "Unknown")
                    details.setdefault("journals", [])
                    details.setdefault("conditions", [])
                    details.setdefault("clinical_notes", "None")
                else:
                    data[role][email] = {
                        "email": email,
                        "password": details,
                        "name": "Unknown",
                        "surname": "Unknown",
                        "date_of_birth": "Unknown",
                        "gender": "Unknown",
                        "NHS_blood_donor": "Unknown",
                        "NHS_organ_donor": "Unknown",
                        "Address_Line_1": "Unknown",
                        "Address_Line_2": "Unknown",
                        "conditions": [],
                        "clinical_notes": "None"
                    }

        if "admin1@gmail.com" not in data["admin"]:
            data["admin"]["admin1@gmail.com"] = {
                "email": "admin1@gmail.com",
                "password": "password1",
                "name": "Default",
                "surname": "Admin",
                "date_of_birth": "Unknown",
                "gender": "Unknown",
                "NHS_blood_donor": "Unknown",
                "NHS_organ_donor": "Unknown",
                "Address_Line_1": "Unknown",
                "Address_Line_2": "Unknown",
                "conditions": [],
                "clinical_notes": "None"
            }
            save_accounts(data)

        return data
    except FileNotFoundError:
        default_data = {
            "patient": {},
            "gp": {"gp1@gmail.com": {
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
                    "clinical_notes": "None"
                }},
            "admin": {
                "admin1@gmail.com": {
                    "email": "admin1@gmail.com",
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
                    "clinical_notes": "None"
                }}}
        # Save the default data to accounts.json
        save_accounts(default_data)
        return default_data

    except Exception as e:
        # Log the error but attempt to recover valid data if possible
        print(f"Error loading accounts: {e}")
        try:
            with open(DATA_FILE, "r") as file:
                partial_data = load(file)
                print("Recovered partial data from corrupted file.")
                return partial_data  # Return what can be recovered
        except Exception as recovery_error:
            print(f"Failed to recover data: {recovery_error}")
            print("Returning a complete default structure.")
            return {
                "patient": {},
                "gp": {},
                "admin": {}
            }
def save_accounts(new_account=None, mode="merge"):
    combined_accounts = {}

    if mode == "merge":
        try:
            # Try to load existing data from the JSON file
            with open(DATA_FILE, "r") as file:
                possible_existing_accounts = load(file)
                combined_accounts.update(possible_existing_accounts)  # Add existing data to combined dictionary
        except FileNotFoundError:
            combined_accounts = {}
        except Exception as e:
            combined_accounts = {}

        # Combine new account information with the existing data
        if new_account:
            for role, accounts in new_account.items():
                # Ensure the role exists in combined_accounts
                if role not in combined_accounts:
                    combined_accounts[role] = {}

                # Merge accounts under this role
                for email, details in accounts.items():
                    if email in combined_accounts[role]:
                        # Merge fields for existing account
                        combined_accounts[role][email].update(details)
                    else:
                        # Add new account
                        combined_accounts[role][email] = details

                    # Ensure all required keys are in the account details
                    combined_accounts[role][email].setdefault("name", "Unknown")
                    combined_accounts[role][email].setdefault("surname", "Unknown")
                    combined_accounts[role][email].setdefault("date_of_birth", "Unknown")
                    combined_accounts[role][email].setdefault("gender", "Unknown")
                    combined_accounts[role][email].setdefault("NHS_blood_donor", "Unknown")
                    combined_accounts[role][email].setdefault("NHS_organ_donor", "Unknown")
                    combined_accounts[role][email].setdefault("Address_Line_1", "Unknown")
                    combined_accounts[role][email].setdefault("Address_Line_2", "Unknown")
                    combined_accounts[role][email].setdefault("journals", [])
                    combined_accounts[role][email].setdefault("conditions", [])
                    combined_accounts[role][email].setdefault("clinical_notes", "None")

    if mode == "override":
        combined_accounts = new_account

    try:
        # Write the combined data back to the JSON file
        with open(DATA_FILE, "w") as file:
            dump(combined_accounts, file, indent=4)
    except Exception as e:
        print(f"Error saving accounts: {e}")
registered_users = load_accounts()
#==========================================================


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
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return load(file)
    except FileNotFoundError:
        return {"patient": {}, "gp": {}, "admin": {}}
def save_data(data):
    with open(DATA_FILE, "w") as file:
        dump(data, file, indent=4)
def manage_gp_details():
    from time import sleep
    # New JSon file, but it only contains new data, have to import all the other GPs from the other accounts.json file
    data_file = "gp_data.json"
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            gp_data = load(file)
    else:
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

    def save_data2():
        with open(data_file, "w") as file:
            dump(gp_data, file, indent=4)
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
        choice9 = input("Enter your choice: ").strip().upper()
        if choice9 == "H":
            print("Returning to the homepage...\n")
            return
        if choice9.isdigit() and 0 < int(choice) <= 10:
            selected_field = list(gp_details.keys())[int(choice) - 1]
            new_value = input(
                f"Enter new {selected_field.replace('_', ' ')} (current: {gp_details[selected_field]}): ").strip()
            if new_value != gp_details[selected_field]:
                while True:
                    confirm = input("Confirm change? (Y/N): ").strip().lower()
                    if confirm == "y":
                        gp_details[selected_field] = new_value
                        save_data2()  # Save the updated data to the file
                        print(f"{selected_field.replace('_', ' ').title()} updated successfully!")
                        break
                    elif confirm == "n":
                        print(f"Change to {selected_field.replace('_', ' ')} discarded.")
                        break
                    else:
                        print("Please input Y or N.")
        else:
            print("Invalid option. Returning to the homepage...\n")
            return
        print("\nUpdated GP Details:")
        for key, value in gp_details.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        save_data2()  # Save the updated data to the file
        print("\nChanges saved successfully!")
    # Function to display options and allow selection of a GP to edit
    while True:
        print("\n[1] Display and Edit GP Details")
        print("[X] Return to Admin Homepage")
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
        elif option.upper() == "X":
            print("Returning to the Admin Homepage...\n")
            break
        else:
            print("Invalid option. Please try again.")
    # Redirect to Admin Homepage
    admins_page()
def manage_gp_system():
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
        elif choice.upper() == 'X':
            admins_page()  # Calls the admin homepage when 'X' is pressed
        else:
            print("Invalid choice. Please try again.")
def manage_accounts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            accounts_data = load(file)
    else:
        accounts_data = {
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
                    "Address_Line_2": "London",
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
            "gp": {},
            "admin": {}
        }
    def update_account_page(email_address):
        patient_data = accounts_data.get("patient", {})
        account_details = patient_data.get(email_address)

        if not account_details:
            print("No patient found with the provided email address.")
            return

        while True:
            print("=" * 80)
            print("Account Details:\n".center(80))
            counter = 1
            keys = list(account_details.keys())
            for key, value in account_details.items():
                print(f"[{counter}] {key[0].upper() + key[1:].replace('_', ' ')}: {value}")
                counter += 1
            print("\n[ H ]  Return to Patient Selection\n")

            update_option = input("Please select an option to edit: ").strip()

            if update_option.upper() == "H":
                print("Returning to patient selection...\n")
                sleep(1)
                break

            if update_option.isdigit() and 0 < int(update_option) <= counter:
                selected_key = keys[int(update_option) - 1]
                new_value = input(f"Enter new value for {selected_key}: ").strip()
                if new_value != account_details[selected_key]:
                    while True:
                        confirm = input("Confirm change? (Y/N): ").strip().lower()
                        if confirm == "y":
                            account_details[selected_key] = new_value
                            accounts_data["patient"][email_address] = account_details
                            save_data(accounts_data)  # Save changes after every update
                            print("Changes saved successfully!")
                            break
                        elif confirm == "n":
                            print("Change discarded.")
                            break
                        else:
                            print("Please input Y or N.")
            else:
                print("\nInvalid input. Please choose a valid option.")



    while True:
        print("\nOptions Menu:")
        print("[1] Display and Edit Patients")
        print("[X] Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            patient_data = accounts_data.get("patient", {})

            if not patient_data:
                print("No patients found.")
                continue

            print("List of Patients:\n")
            for index, (email, details) in enumerate(patient_data.items(), start=1):
                print(f"[{index}] Name: {details['name']} {details['surname']}, Email: {email}")

            while True:
                try:
                    selection = input(
                        "\nEnter the number of the patient to edit (or 'H' to return to main menu): ").strip()
                    if selection.upper() == "H":
                        print("Returning to main menu...\n")
                        break
                    patient_index = int(selection)
                    if 1 <= patient_index <= len(patient_data):
                        selected_email = list(patient_data.keys())[patient_index - 1]
                        update_account_page(selected_email)
                        break
                    else:
                        print("Invalid selection. Please choose a valid number.")
                except ValueError:
                    print("Invalid input. Please enter a number or 'H'.")
        elif choice.upper() == "X":
            print("Exiting the programme")
            break
        else:
            print("Invalid choice. Please try again.")
def display_summary_info_system():

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            json_data = json.load(file)
    else:
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
                "Address_Line_2": "London",
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
        "gp": {
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
        **json_data["gp"],
    }

    def list_users():
        """Display all users and allow the user to select one to view details."""
        while True:
            print("\nList of Users:")
            user_list = list(users.items())
            for idx, (email, data) in enumerate(user_list, 1):
                user_type = "Patient" if email in json_data["patient"] else "MHWP"
                full_name = f"{data['name']} {data['surname']}"
                print(f"[{idx}] {full_name} ({user_type})")

            # Select a user
            while True:
                choice = input("\nSelect a user to view details (or X to return to Admin Homepage): ")
                if choice.upper() == 'X':
                    print("Returning to Admin Homepage...")
                    admins_page()
                elif 1 <= choice <= len(user_list):
                    email, data = user_list[choice - 1]
                    view_user_details(email, data)
                    break
                else:
                    print("Invalid choice. Please choose a valid option '1' or 'X'.")

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

        print("\nPress Enter to return to 'List of Users'.")
        input()
        list_users()
#==========================================================


#====================Patient Homepage======================

#[ 1 ] Book and manage appointments
def book_and_manage_appointments(email_address):
    print("[ 1 ] View upcoming appointments")
    print("[ 2 ] Book an appointment")
    print("[ 3 ] Cancel appointment")
    print("[ M ] Return to Main menu")
    while True:
        choice1 = input("\nPlease select an option: ").strip()
        if choice1.upper() == "M":
            patients_page(email_address=email_address)
        elif choice1 == "1":
            view_patient_schedule(email_address)
        elif choice1 == "2":
            book_appointment(email_address, "gp1@gmail.com")  # Need to wait for GP-Patient pairings
        elif choice1 == "3":
            cancel_patient_appointment(email_address)
        else:
            print("Please choose a valid option '1' , '2' , '3' or 'M'")
def view_patient_schedule(patient_email):
    conn = sqlite3.connect('appointments.db')
    cursor = conn.cursor()

    query = """
    SELECT id, date, time_slot, appointment_status
    FROM appointments
    WHERE patient_email = ?
    ORDER BY date, time_slot;
    """
    cursor.execute(query, (patient_email,))
    rows = cursor.fetchall()

    if rows:
        print("Your Appointments:")
        table = []
        headers = ["Slot ID", "Date", "Time Slot", "Status"]

        for row in rows:
            table.append(row)

        print(tabulate.tabulate(table, headers=headers, tablefmt='grid'))
        conn.close()

        print("[ 1 ] Cancel appointment")
        print("[ M ] Return to Main menu")
        while True:
            c = input("\nPlease select an option: ")
            if c.upper() == "M":
                patients_page(patient_email)
            elif c == "1":
                cancel_patient_appointment(patient_email)

    print("You have no appointments booked.\nReturning to main menu...")
    conn.close()
    sleep(2)
    patients_page(patient_email)
def book_appointment(patient_email, gp_email):

    conn = sqlite3.connect('appointments.db')
    cursor = conn.cursor()

    # Check if the patient already has an appointment
    cursor.execute("""
    SELECT id FROM appointments WHERE patient_email = ?;
    """, (patient_email,))
    existing_appointment = cursor.fetchone()

    if existing_appointment:
        print("You already have an appointment booked. Cancel it first to book a new one.")
        conn.close()
        patients_page(patient_email)

    while True:
        start_date_input = input("Enter the start date of the week (YYYY-MM-DD): ").strip()
        try:
            start_date = datetime.strptime(start_date_input, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    end_date = start_date + timedelta(days=6)
    schedule = {}  # Dictionary to store time slots for each date

    query = """
    SELECT id, date, time_slot
    FROM appointments
    WHERE patient_email IS NULL 
      AND appointment_status = 'Available'
      AND gp_email = ?
      AND date BETWEEN ? AND ?
    ORDER BY date, time_slot;
    """
    cursor.execute(query, (gp_email, str(start_date), str(end_date)))
    available_slots = cursor.fetchall()

    if not available_slots:
        print("No available appointments for the selected week.\nReturning to main menu...")
        conn.close()
        sleep(2)
        patients_page(patient_email)

    time_slots = sorted(set(slot[2] for slot in available_slots))  # Unique time slots
    for time_slot in time_slots:
        schedule[time_slot] = {str(start_date + timedelta(days=i)): "Unavailable" for i in range(7)}

    for slot_id, date, time_slot in available_slots:
        schedule[time_slot][date] = f"[{slot_id}]"

    headers = ["Time Slot"] + [str(start_date + timedelta(days=i)) for i in range(7)]
    table = [[time_slot] + [schedule[time_slot][date] for date in headers[1:]] for time_slot in time_slots]
    print("\nGP's Weekly Schedule:")
    print(tabulate.tabulate(table, headers=headers, tablefmt="grid"))

    # Allow patient to select a slot to book by Slot ID
    while True:
        slot_id_input = input("Enter the [Slot ID] to book (or 'Q' to quit): ").strip()
        if slot_id_input.upper() == 'Q':
            print("Booking process cancelled.\nReturning to Main menu...")
            patients_page(patient_email)

        try:
            slot_id = int(slot_id_input)
            cursor.execute("""
                SELECT id FROM appointments 
                WHERE id = ? AND gp_email = ? AND patient_email IS NULL AND appointment_status = 'Available';
            """, (slot_id, gp_email))
            valid_slot = cursor.fetchone()

            if valid_slot:
                cursor.execute("""
                    UPDATE appointments
                    SET patient_email = ?, appointment_status = 'Requested'
                    WHERE id = ?;
                """, (patient_email, slot_id))
                conn.commit()
                print(f"Appointment booked successfully! [Slot ID]: {slot_id}\nreturning to Main menu...")
                sleep(2)
                patients_page(patient_email)
            else:
                print("Invalid Slot ID or the slot is no longer available. Try again.")
        except ValueError:
            print("Invalid input. Please enter a valid Slot ID.")

    conn.close()
def cancel_patient_appointment(patient_email):

    conn = sqlite3.connect('appointments.db')
    cursor = conn.cursor()

    # Query to fetch the patient's appointment
    query = """
    SELECT id, date, time_slot, gp_email, appointment_status
    FROM appointments
    WHERE patient_email = ?
    ORDER BY date, time_slot;
    """
    cursor.execute(query, (patient_email,))
    rows = cursor.fetchall()

    if not rows:
        print("You have no booked appointments to cancel.\nReturning to Main menu...")
        conn.close()
        sleep(2)
        patients_page(patient_email)

    # Display the appointment(s) in a table
    table = []
    headers = ["Slot ID", "Date", "Time Slot", "GP Email", "Status"]

    for row in rows:
        table.append(row)

    print("\nYour Booked Appointments (Requested and Confirmed):")
    print(tabulate.tabulate(table, headers=headers, tablefmt='grid'))

    # Allow patient to select an appointment to cancel
    valid_ids = {row[0] for row in rows}  # Set of valid Slot IDs
    while True:
        cancel = input("\nEnter Slot ID to cancel (or 'Q' to quit): ").strip()
        if cancel.upper() == 'Q':
            print("\nReturning to Main menu...")
            conn.close()
            patients_page(patient_email)

        try:
            slot_id = int(cancel)
            if slot_id in valid_ids:
                confirm = input(f"Are you sure you want to cancel appointment {slot_id}? (y/n): ").strip().lower()
                if confirm == 'y':
                    cursor.execute("""
                    UPDATE appointments
                    SET patient_email = NULL, appointment_status = 'Available'
                    WHERE id = ? AND patient_email = ?;
                    """, (slot_id, patient_email))
                    conn.commit()
                    print(f"Appointment {slot_id} has been canceled.")
                    valid_ids.remove(slot_id)
                else:
                    print("Cancellation aborted.")
            else:
                print("Invalid Slot ID. Please choose a valid Slot ID from the table.")
        except ValueError:
            print("Invalid input. Please enter a valid Slot ID.")

#[ 2 ] Change default GP

#[ 3 ] Access meditation help & tips and more
resources = {
    "Breathing Practices": {
        1: ("3 minute breathing practice", "https://drive.google.com/file/d/1nzkNZ9r2SWWn86NTDykEkCj4HosAgfGb/view"),
        2: ("5 minute breathing practice", "https://drive.google.com/file/d/1eucLhrVRBT7FCTzdbpns7MCLb4PILK0t/view"),
        3: ("10 minute breathing practice", "https://drive.google.com/file/d/1hGEntCirailnpjSlX4ZgGVbmd-qAQHr8/view"),
    },
    "Help with Sleep": {
        1: ("Guided Imagery for Sleep by Dan Guerra", "https://insighttimer.com/danguerra/guided-meditations/guided-imagery-for-sleep-3"),
        2: ("Progressive Relaxation Nidra by Ally Boothroyd", "https://insighttimer.com/allyboothroyd/guided-meditations/progressive-relaxation-nidra"),
        3: ("Guided Meditation For Deep Sleep by Daphne Lyon", "https://insighttimer.com/daphnelyon/guided-meditations/guided-meditation-for-deep-sleep-4"),
        4: ("A Guided Visualization Meditation For Deep & Restful Sleep", "https://insighttimer.com/movie123man/guided-meditations/a-guided-visualization-meditation-for-deep-and-restful-sleep"),
    },
    "Help with Anxiety": {
        1: ("Decrease Anxiety & Increase Peace by Andrea Wachter", "https://insighttimer.com/andreawachter/guided-meditations/decrease-anxiety-and-increase-peace"),
        2: ("Guided Meditation For Anxiety Relief by Elisa (Ellie) Bozmarova", "https://insighttimer.com/elliebozmarova/guided-meditations/guided-meditation-for-anxiety-relief"),
    },
    "Gratitude": {
        1: ("Five-Minute Morning Practice On Gratitude by Julie Ela Grace", "https://insighttimer.com/julieelagrace/guided-meditations/five-minute-morning-meditation-on-gratitude"),
        2: ("Gratitude Affirmations For The Body And Life by Julie Ela Grace", "https://insighttimer.com/julieelagrace/guided-meditations/gratitude-affirmations-for-the-body-and-life"),
    },
    "Stress & Burnout": {
        1: ("Quick Stress Release by Saqib Rizvi", "https://insighttimer.com/saqibrizvi/guided-meditations/quick-stress-release"),
        2: ("Relief From Stress & Pressure by Mary Maddux", "https://insighttimer.com/meditationoasis/guided-meditations/relief-from-stress-and-pressure"),
    },
}
def mhresources(email_address):
    """Function to display the main menu and navigate categories."""
    while True:
        print("\nAvailable Categories:")
        for num, category in enumerate(resources.keys(), 1):
            print(f"{num}. {category}")
        print("Type 'E' to return to the patient homepage.")

        user_input = input("Enter the number corresponding to the category: ").strip().lower()

        if user_input.upper() == "E":
            patients_page(email_address)

        # Validate category selection
        try:
            category_num = int(user_input)
            if 1 <= category_num <= len(resources):
                category_name = list(resources.keys())[category_num - 1]
                return category_menu(category_name, email_address)
            else:
                print("Invalid input. Please choose a valid category number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
def category_menu(category_name, email_address):
    """Function to display links for the selected category."""
    print(f"\n{category_name} Resources:")
    category_resources = resources[category_name]
    for num, (description, _) in category_resources.items():
        print(f"{num}. {description}")
    print("Type 'B' to return to the main menu.")

    while True:
        user_input = input("Enter the number corresponding to the resource: ").strip().lower()

        if user_input.upper() == "B":
            mhresources(email_address=email_address)

        # Validate resource selection
        try:
            resource_num = int(user_input)
            if resource_num in category_resources:
                resource_description, resource_link = category_resources[resource_num]
                print(f"The link for '{resource_description}' is: {resource_link}")
                post_selection(category_name, email_address)  # Follow-up after showing the link
            else:
                print("Invalid input. Please choose a valid resource number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
def post_selection(category_name, email_address):
    """Function to follow up after a resource selection."""
    print("\nWe hope this resource was helpful.")
    print("1. Explore more resources in this category.")
    print("2. Explore other categories.")
    print("Type 'B' to return to the patient homepage, if further support is needed.")

    while True:
        user_input = input("Enter the number corresponding to your choice or type 'back': ").strip().lower()

        if user_input == "1":
            return category_menu(category_name, email_address)
        elif user_input == "2":
            mhresources(email_address=email_address)
        elif user_input.upper() == "B":
            patients_page(email_address=email_address)
        else:
            print("Invalid input. Please enter a valid option.")

#[ 4 ] Access journal entries
def journal_page(email_address):
    while True:
        print("=" * 80)
        print("JOURNALS PAGE".center(80))
        print("[ 1 ] Make a new journal entry")
        print("[ 2 ] View previous journal entries")
        print("[ 3 ] Edit previous journal entries")
        print("[ 4 ] Delete previous journal entries")
        print("[ H ] Return to your homepage")
        choice = input("\nPlease select an option: ").strip().upper()
        if choice == "1":
            new_journal_entry(email_address)
        elif choice == "2":
            view_journal_entries(email_address)
        elif choice == "3":
            edit_journal_entries(email_address)
        elif choice == "4":
            delete_journal_entries(email_address)
        elif choice == "H":
            print("Returning to your homepage...")
            sleep(1)
            patients_page(email_address)
            break
        else:
            print("Invalid choice, please select '1', '2', '3', '4' or 'H' ")
def new_journal_entry(email_address):
    print("\nPlease write your journal entry. Type 'SAVE' on a new line to save your entry. ")
    entry_line = []
    while True:
        line = input()
        if line.strip().upper() == "SAVE":
            break
        else:
            entry_line.append(line)
    entry_text = "\n".join(entry_line)
    if not entry_text.strip():
        print("Empty journal entry. Not saved")
        return

    entry_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data=load_accounts()
    patient_account = data["patient"][email_address]
    journal_entry = {
        "date": entry_date,
        "entry": entry_text
    }

    if 'journals' not in patient_account:
        patient_account['journals'] = []
    patient_account['journals'].append(journal_entry)


    save_accounts(data, mode= 'override')

    print("Your journal entry has been saved")
    print("Returning to your journals page... ")
    sleep(1)
    journal_page(email_address)
def view_journal_entries(email_address):
    data = load_accounts()
    patient_account = data["patient"][email_address]
    journals = patient_account.get("journals", [])
    if not journals:
        print("\nYou have no journal entries. ")
        while True:
            new_journal = input("\nWould you like to write your first journal entry? (Y/N) ").strip().upper()
            if new_journal == "Y":
                new_journal_entry(email_address)
                break
            elif new_journal == "N":
                print("Returning to your journals page...")
                sleep(1)
                journal_page(email_address)
                break
            else:
                print("Invalid choice. Please choose either Y or N")
        return
    journals_sorted = sorted(journals, key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d %H:%M:%S"))

    print("Loading your previous journal entries...")
    sleep(2)
    print("\nYour Journal Entries:")
    for idx, journal in enumerate(journals_sorted, start=1):
        print(f"\nEntry {idx} - Date: {journal['date']}")
        print("-" * 40)
        print(journal['entry'])
        print("-" * 40)
        sleep(1)
    while True:
        new_journal = input("Would you like to add another journal entry? (Y/N) ").strip().upper()
        if new_journal == "Y":
            new_journal_entry(email_address)
            break
        elif new_journal == "N":
            print("Returning to your journals page...")
            sleep(1)
            journal_page(email_address)
            break
        else:
            print("Invalid choice. Please choose either Y or N")
def edit_journal_entries(email_address):
    data = load_accounts()
    patient_account = data["patient"][email_address]
    journals = patient_account.get("journals", [])
    if not journals:
        print("\nYou have no journal entries to edit")
        print("Returning to your journals page...")
        sleep(2)
        journal_page(email_address)
        return

    journals_sorted = sorted(journals, key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d %H:%M:%S"))
    print("Fetching your previous journal entries...")
    sleep(2)
    print("Your Journal Entries: ")
    for idx, journal in enumerate(journals_sorted, start=1):
        print(f"\nEntry {idx} - Date: {journal['date']}")
        print("-" * 40)
        print(journal['entry'])
        print("-" * 40)
        sleep(1)

    while True:
        choice = input(
            "\nEnter the number of the entry you wish to edit (or 'B' to go back to the journals page): ").strip()
        if choice.upper() == "B":
            print("Returning to your journals page...")
            sleep(1)
            journal_page(email_address)
        try:
            entry_num = int(choice)
            if 1 <= entry_num <= len(journals_sorted):
                break
            else:
                print("Invalid entry number.")
        except ValueError:
            print("Please enter a valid number.")

    selected_journal = journals_sorted[entry_num - 1]

    print("\nCurrent entry: \n")
    print(selected_journal['entry'])

    print("\nEnter your new journal entry. Type 'SAVE' on a new line to save your entry.")
    new_entry_lines = []
    while True:
        line = input()
        if line.strip().upper() == "SAVE":
            break
        else:
            new_entry_lines.append(line)
    new_entry_text = "\n".join(new_entry_lines)
    if not new_entry_text.strip():
        print("Empty journal entry. No changes made. ")
        return
    selected_journal['entry'] = new_entry_text
    data["patient"][email_address]["journals"] = journals
    save_accounts(data, mode="override")
    print("Saving your changes..")
    sleep(1)
    print("Your journal entry has been updated.")
    sleep(1)
    print("Returning to your journals page...")
    sleep(1)
    journal_page(email_address)
def delete_journal_entries(email_address):
    data = load_accounts()
    patient_account = data["patient"][email_address]
    journals = patient_account.get("journals", [])
    if not journals:
        print("\nYou have no journal entries to edit")
        print("Returning to your journals page...")
        sleep(2)
        journal_page(email_address)
        return

    journals_sorted = sorted(journals, key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d %H:%M:%S"))
    print("Fetching your previous journal entries...")
    sleep(2)
    print("Your Journal Entries: ")
    for idx, journal in enumerate(journals_sorted, start=1):
        print(f"\nEntry {idx} - Date: {journal['date']}")
        print("-" * 40)
        print(journal['entry'])
        print("-" * 40)
        sleep(1)

    while True:
        choice = input(
            "\nEnter the number of the entry you wish to edit (or 'B' to go back to the journals page): ").strip()
        if choice.upper() == "B":
            print("Returning to your journals page...")
            sleep(1)
            journal_page(email_address)
        try:
            entry_num = int(choice)
            if 1 <= entry_num <= len(journals_sorted):
                break
            else:
                print("Invalid entry number.")
        except ValueError:
            print("Please enter a valid number.")

    selected_journal = journals_sorted[entry_num - 1]

    print("\nCurrent entry: \n")
    print(selected_journal['entry'])

    confirm= input("\nAre you sure you want to delete this entry? (Y/N) ").strip().upper()
    if confirm == "Y":
        journals.remove(selected_journal)
        data["patient"][email_address]["journals"] = journals
        save_accounts(data, mode="override")
        print("Saving your changes...")
        sleep(1)
        print("Your journal entry has been deleted.")
    else:
        print("\nDeletion cancelled.")
    print("Returning to your journals page...")
    sleep(1)
    journal_page(email_address)

# [ 5 ] Change patient details
def update_account_page(email_address):
    data = load_accounts()
    account_details = data["patient"][email_address]
    updates_made = False

    while True:
        print("="*80)
        print("Account Details:\n".center(80))
        counter = 1
        for key, value in account_details.items():
            if key != "password" and key!= "journals" and key!= "conditions" and key!= "clinical_notes" :
                print("[", counter, "] ", (key[0].upper()) + key[1:len(key)].replace("_", " "), ": ", value)
                counter += 1
        print("\n[ H ]  Go to Homepage\n")
        # print("\n")


        update_option = input("Please select an option to edit: ").strip()

        if update_option.upper() == "H":
            print("Returning to your homepage...\n")
            sleep(1)
            patients_page(email_address)
            break

        if update_option.isdigit() and 0 <= int(update_option) <= 9:
            update_option = int(update_option)
        else:
            print("\n")
            print("Invalid input. Please choose a valid option")
            continue


        if update_option == 1:
            while True:
                new_email = input("Please enter your new email address: ").strip()
                email_pattern = r"^[\w\.-]+@[\w\.-]+\.[\w\.-]+$"

                if new_email.upper() == "E":
                    break

                if new_email == email_address:
                    print("This is already your current email. ")
                    break

                if new_email in data["patient"] and new_email != email_address:
                    print("This is already your current email. No changes made. ")
                    break


                elif match(email_pattern,new_email):

                    reset_code = str(randint(100000, 999999))
                    print(f"To verify the new email address, a verification code will be sent to the email. Simulated reset code {new_email}: {reset_code}")

                    for attempt in range(4):
                        user_code = input("Enter the reset code sent to your email: ")
                        if user_code == reset_code:
                            break
                        else:
                            print("Incorrect code. Please try again")
                            if attempt == 3:
                                print("Too many incorrect attempts. No change has been made to your account. Returning to your homepage...\n")
                                sleep(2)
                                patients_page(email_address)
                                return

                    account_details["email"] = new_email
                    del data["patient"][email_address]
                    data["patient"][new_email] = account_details
                    email_address= new_email
                    updates_made=True
                    break
                else:
                    print("Invalid email format. Please enter a valid email.")

        elif update_option == 2:
            new_first_name = input("Please enter your new first name: ").strip()
            if new_first_name != account_details["name"]:
                while True:
                    final_confirmation = input("Please confirm you would like to make this change to your account (Y/N): ").strip().lower()
                    if final_confirmation == "y":
                        account_details["name"] = new_first_name
                        updates_made = True
                        break

                    elif final_confirmation == "n":
                        # print("Returning to your patient homepage...")
                        # sleep(1)
                        # patients_page(email_address)
                        break

                    else:
                        print("Please input a valid option, either Y or N. ")

            else:
                print("This is already your current first name.")



        elif update_option == 3:
            new_surname = input("Please enter your new surname: ").strip()
            if new_surname != account_details["surname"]:
                while True:
                    final_confirmation = input("Please confirm you would like to make this change to your account (Y/N): ").strip().lower()
                    if final_confirmation == "y":
                        account_details["surname"] = new_surname
                        updates_made = True
                        break

                    elif final_confirmation == "n":
                        break
                        # print("Returning to your patient homepage...")
                        # sleep(1)
                        # patients_page(email_address)


                    else:
                        print("Please input a valid option, either Y or N ")

            else:
                print("This is already your current surname")


        elif update_option == 4:
            while True:
                new_birthday = input("Birth date (DD/MM/YYYY): ").strip()  # Pad single digit day with zero if necessary

                if new_birthday.upper() == "E":
                    break

                if new_birthday != account_details["date_of_birth"]:
                    try:
                        day, month, year = map(int, new_birthday.split("/"))
                        datetime(year,month,day)
                        account_details["date_of_birth"] = new_birthday
                        updates_made= True
                        break
                    except ValueError:
                        print("Invalid birth date. Please enter in the format DD/MM/YYYY.")
                else:
                    print("This is already your current date of birth.")
                    break


        elif update_option == 5:
            while True:
                print("Genders:")
                print("[ 1 ] Male")
                print("[ 2 ] Female")

                new_gender_option = input("Please choose an option: ").strip()
                if new_gender_option == "1":
                    new_gender = "Male"
                elif new_gender_option == "2":
                    new_gender = "Female"
                elif new_gender_option.upper() == "E":
                    break
                else:
                    print("Please choose a valid option '1' or '2' ")

                if new_gender != account_details["gender"]:
                    account_details["gender"] = new_gender
                    updates_made= True
                    break
                else:
                    print("Please choose a valid option '1' or '2' ")
                    break


        elif update_option == 6:
            while True:
                print("NHS blood donor: ")
                print("[ 1 ] Yes")
                print("[ 2 } No")
                donor_new = input("Please choose an option: ").strip()
                if donor_new == "1":
                    donor_new = "IS Blood donor"
                elif donor_new == "2":
                    donor_new = "NOT Blood donor"
                elif donor_new.upper() == "E":
                    break
                else:
                    print("Invalid choice, Please choose 1 or 2")
                    continue

                if donor_new != account_details["NHS_blood_donor"]:
                    account_details["NHS_blood_donor"] = donor_new
                    updates_made = True
                    break
                else:
                    print("This is already your current NHS blood donor status")
                    break


        elif update_option == 7:

            while True:
                print("NHS organ donor:")
                print("[ 1 ] Yes")
                print("[ 2 } No")
                organ_new = input("Please choose an option: ").strip()
                if organ_new == "1":
                    organ_new = "IS Organ donor"
                elif organ_new == "2":
                    organ_new = "NOT Organ donor"
                elif organ_new.upper() == "E":
                    break
                else:
                    print("Invalid choice. Please choose 1 or 2")
                    continue


                if organ_new != account_details["NHS_organ_donor"]:
                    account_details["NHS_organ_donor"] = organ_new
                    updates_made= True
                    break
                else:
                    print("This is already your current NHS organ donor status")
                    break


        elif update_option == 8:

            ad1_new = input("Please enter a new Address Line 1: ")
            if ad1_new != account_details["Address_Line_1"]:
                while True:
                    final_confirmation = input("Please confirm you would like to make this change to your account (Y/N): ").strip().lower()
                    if final_confirmation == "y":
                        account_details["Address_Line_1"] = ad1_new
                        updates_made = True
                        break

                    elif final_confirmation == "n":
                        break
                        # print("Returning to your patient homepage...")
                        # sleep(1)
                        # patients_page(email_address)

                    else:
                        print("Please input a valid option, either Y or N. ")

            else:
                print("This is already your current Address Line 2.")


        elif update_option == 9:
            ad2_new = input("Please enter a new Address Line 2: ")
            if ad2_new != account_details["Address_Line_2"]:
                while True:
                    final_confirmation = input("Please confirm you would like to make this change to your account (Y/N): ").strip().lower()
                    if final_confirmation == "y":
                        account_details["Address_Line_2"] = ad2_new
                        updates_made = True
                        break

                    elif final_confirmation == "n":
                        break
                        # print("Returning to your patient homepage...")
                        # sleep(1)
                        # patients_page(email_address)

                    else:
                        print("Please input a valid option, either Y or N. ")
            else:
                print("This is already your current Address Line 2.")

        else:
            print("Invalid option")
            continue



        if updates_made:
            data["patient"][email_address]= account_details
            with open("accounts.json","w") as file:
                dump(data , file ,indent=4)
            print("Updating your account details...")
            sleep(1)
            print("Your changes have been saved successfully!")
            sleep(1)
            updates_made = False

        else:
            print("\nNo changes were made.\n")
            sleep(1)

        print("-"*80)
        print("Updated account details:")
        print("")
        for key,value in account_details.items():
            if key != "password" and key!= "journals" and key!= "conditions" and key!= "clinical_notes" :
                print((key[0].upper()) + key[1:len(key)].replace("_", " "), ": ", value)

        print("\n")
        edit_again= input("Would you like to edit another detail? (Y/N): ").strip().lower()
        if edit_again == "n":
            print("\nReturning to your homepage...")
            sleep(1)
            patients_page(email_address)
            break
        elif edit_again!= "y":
            print("Returning to the edit menu")

# [ 6 ] Helplines
def helplines(email_address):
    print("=" * 80)
    print("HELPLINES".center(80))
    print("""\n\033[1mIf it's an emergency or you need urgent help:\033[0m\n""")
    print("""- If you or someone else is in danger, call \033[1m\033[4m999\033[0m\033[0m or go to A&E now""")
    print("""- If you need urgent help for your mental health, get help call \033[1m\033[4m111\033[0m\033[0m
      www.nhs.uk""")
    print("-" * 80)
    print("""Experiencing a mental health problem or supporting someone else - www.sane.org.uk
    Call: \033[1;4m0300 304 7000\033[0m (4.30pm–10pm every day)""")
    print("-" * 80)
    print("""Suicide Prevention Helpline UK - www.spuk.org.uk
    Call: \033[1;4m0800 689 5652\033[0m (6pm to midnight every day)""")
    print("-" * 80)
    print("""Samaritans (distressed, despaired or having suicidal thought) - www.samaritans.org
    Call: \033[1;4m0808 164 0123\033[0m (7pm–11pm every day) or \033[1;4m116 123\033[0m (24 hours a day)""")
    print("-" * 80)
    print("""Parents helpline - www.youngminds.org.uk
    Call: \033[1;4m0808 802 5544\033[0m (Mon-Fri from 9.30am to 4pm)""")
    print("-" * 80)
    print("""Severe mental illness (schizophrenia, bipolar disorder) - www.rethink.org
    Call: \033[1;4m0300 5000 927\033[0m (9:30am to 4pm, Monday to Friday)""")
    print("-" * 80)
    print("""General mental health support - www.mind.org.uk
    Call: \033[1;4m0300 123 3393\033[0m (9am to 6pm, Monday to Friday), or text \033[1;4m86463\033[0m""")
    print("-" * 80)
    sleep(2)
    print("\nIf you can't talk on the phone:")
    print("""
\033[1mList of mental health helplines\033[0m from the Helplines Partnership
(https://www.helplines.org/helplines/?fwp_topics=mental-health)

\033[1mMental Health Foundation\033[0m provides useful information on a range of mental health difficulties, as well as resources to support your wellbeing 
(https://www.mentalhealth.org.uk/explore-mental-health/publications)

\033[1mMentally Healthy\033[0m Schools has a wide range of information for schools and teachers to support young people’s mental health 
(https://www.mentallyhealthyschools.org.uk/)

\033[1mMental Health and Money Advice\033[0m provides practical advice and support for people experiencing issues with mental health and money 
(https://www.mentalhealthandmoneyadvice.org/)

\033[1mMe and My Mind\033[0m has some useful information for young people who may be having unusual experiences, such as paranoia or hearing voices 
(https://www.meandmymind.nhs.uk/)
    """)
    print("\nEnter 'M' to return to main menu ")
    while True:
        pick = input("").strip()
        if pick.upper() == "M":
            print("Returing to main menu..\n")
            patients_page(email_address)
        else:
            continue
#==========================================================


#=======================GP Homepage========================
# [ 1 ] View schedule
def view_gp_schedule(gp_email):
    conn = sqlite3.connect('appointments.db')
    cursor = conn.cursor()

    query = """
    SELECT id, date, time_slot, patient_email, appointment_status
    FROM appointments
    WHERE gp_email = ?
    ORDER BY date, time_slot;
    """
    cursor.execute(query, (gp_email,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No appointments scheduled.\nReturning to Main menu...")
        sleep(2)
        gp_page(gp_email)

    table = []
    headers = ["Slot ID", "Date", "Time Slot", "Patient Email", "Status"]

    for row in rows:
        table.append(row)

    print(tabulate.tabulate(table, headers=headers, tablefmt='grid'))
    print("\n[ 1 ] View by week")
    print("[ M ] Return to Main menu")
    while True:
        c2 = input("\nPlease choose an option: ")
        if c2.upper() == "M":
            gp_page(gp_email)
        elif c2 == "1":
            view_gp_schedule_by_week(gp_email)
        else:
            print("Please choose a valid option '1' or 'M'")
def view_gp_schedule_by_week(gp_email):
    """
    Allows the GP to view their schedule for a specific week, starting from a chosen day.
    Displays the schedule in a 5-day format with time slots and patient emails.
    """
    # Ask the GP for the start date of the week
    while True:
        try:
            start_date_str = input("Enter the start date of the week (YYYY-MM-DD): ").strip()
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")


    end_date = start_date + timedelta(days=4)  # End date is 4 days after the start date

    conn = sqlite3.connect('appointments.db')
    cursor = conn.cursor()

    # Query appointments for the given GP and the week (5 days)
    query = """
    SELECT id, date, time_slot, patient_email, appointment_status
    FROM appointments
    WHERE gp_email = ? AND date BETWEEN ? AND ?
    ORDER BY date, time_slot;
    """
    cursor.execute(query, (gp_email, start_date, end_date))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print(f"No appointments scheduled for the week starting {start_date}.\n")
        print("[ 1 ] View a different week schedule")
        print("[ M ] Return to Main menu")
        while True:
            c4 = input("Please select an option: ")
            if c4.upper() == "M":
                gp_page(gp_email)
            elif c4 == "1":
                view_patient_schedule(gp_email)
            else:
                print("Please choose a valid option '1' or 'M'")

    # Prepare the schedule in a week-view format (5 days)
    schedule = {}
    for row in rows:
        slot_id, date, time_slot, patient_email, appointment_status = row
        if date not in schedule:
            schedule[date] = {}
        schedule[date][time_slot] = patient_email if patient_email else None

    # Generate a 5-day table to view the schedule
    headers = ["Time Slot", *[start_date + timedelta(days=i) for i in range(7)]]
    table = []

    # Define the full list of time slots, including 16:30
    time_slots = ['09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30',
                  '14:00', '14:30', '15:00', '15:30', '16:00', '16:30']

    for time_slot in time_slots:
        row = [time_slot]
        for day in range(7):
            date_to_check = start_date + timedelta(days=day)
            email = schedule.get(date_to_check, {}).get(time_slot, None)
            if email:
                row.append(f"{email}")
            else:
                row.append("")
        table.append(row)

    # Print the schedule
    print(tabulate.tabulate(table, headers=headers, tablefmt='grid', stralign='center'))
    print("\n[ 1 ] To view a different week")
    print("[ M ] Return to main menu")
    while True:
        c3 = input("Please select an option: ")
        if c3.upper() == "M":
            gp_page(gp_email)
        elif c3 == "1":
            view_gp_schedule_by_week(gp_email)
        else:
            print("Please choose a valid option '1' or 'M'")

# [ 2 ] Manage appointments
def manage_appointments(gp_email):
    print("\n")
    print("[ 1 ] View upcoming appointments")
    print("[ 2 ] Confirm appointments")
    print("[ 3 ] Cancel appointments")
    print("[ M ] Return to Main menu")
    while True:
        c6 = input("Please select an option: ").strip()
        if c6.upper() == "M":
            gp_page(gp_email)
        elif c6 == "1":
            view_upcoming_appointments(gp_email)
        elif c6 == "2":
            confirm_appointments(gp_email)
        elif c6 == "3":
            cancel_gp_appointment(gp_email)
        else:
            print("Please choose a valid option '1' , '2' , '3' or 'M'")
def setup_database():
    """
    Sets up the database with the appointments table.
    Creates the table if it doesn't exist.
    """
    conn = sqlite3.connect('appointments.db')
    cursor = conn.cursor()

    # Create the appointments table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gp_email TEXT NOT NULL,
        patient_email TEXT, -- Null if the slot is not booked
        date TEXT NOT NULL,
        time_slot TEXT NOT NULL,
        appointment_status TEXT NOT NULL, -- "Booked" or "Available"
        FOREIGN KEY (gp_email) REFERENCES gp (email)
    );
    """)
    conn.commit()
    conn.close()
def initialize_database():
    """
    Initializes the database. Checks if the database file exists;
    if not, sets up the database structure.
    """
    if not os.path.exists("appointments.db"):
        setup_database()  # Run setup if the file does not exist
        #print("Database initialized successfully.")
    #else:
        #print("Loading current appointments database...")
        #sleep(1)
        #print("Done!")
def update_time_slots():

    connection = sqlite3.connect("appointments.db")
    cursor = connection.cursor()

    # Get the current date
    today = datetime.now().date()

    # Delete past slots
    cursor.execute("""
        DELETE FROM appointments
        WHERE date < ?
    """, (str(today),))
    #print(f"Deleted past time slots before {today}.")

    cursor.execute("""
        SELECT MAX(date) FROM appointments
    """)
    latest_date = cursor.fetchone()[0]

    # Calculate the number of days to add
    if latest_date:
        latest_date = datetime.strptime(latest_date, "%Y-%m-%d").date()
    else:
        latest_date = today - timedelta(days=1)  # If no slots exist, start from today

    days_to_add = (today + timedelta(days=90)) - latest_date

    # Add new days to ensure 90 days of slots
    if days_to_add.days > 0:
        for day in (latest_date + timedelta(days=i + 1) for i in range(days_to_add.days)):
            # Skip weekends
            if day.weekday() in (5, 6):
                continue

            # Add new slots for this date for all GPs
            cursor.execute("""
                SELECT DISTINCT gp_email FROM appointments
            """)
            gp_emails = [row[0] for row in cursor.fetchall()]

            time_slots = [f"{hour:02d}:{minute:02d}" for hour in range(9, 17) for minute in (0, 30)]
            for gp_email in gp_emails:
                for slot in time_slots:
                    cursor.execute("""
                        INSERT INTO appointments (date, time_slot, gp_email, patient_email, appointment_status)
                        VALUES (?, ?, ?, NULL, "Available")
                    """, (str(day), slot, gp_email))
        #print(f"Added {days_to_add.days} new days of slots up to {today + timedelta(days=90)}.")

    # Commit changes and close the connection
    connection.commit()
    connection.close()
def initialize_and_populate_new_gp_slots():
    """
    Initializes and populates time slots for GPs with no existing slots in the database.
    """
    connection = sqlite3.connect("appointments.db")
    cursor = connection.cursor()

    # Get all GP emails
    with open("accounts.json", "r") as f:
        accounts = load(f)
        gp_emails = [gp["email"] for gp in accounts["gp"].values()]

    # Get GPs already in the database
    cursor.execute("""
        SELECT DISTINCT gp_email FROM appointments
    """)
    existing_gps = {row[0] for row in cursor.fetchall()}

    # Filter GPs without existing slots
    new_gps = set(gp_emails) - existing_gps

    # Populate time slots for each new GP
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=90)

    for gp_email in new_gps:
        print(f"Populating slots for new GP: {gp_email}")
        for day in (start_date + timedelta(days=i) for i in range((end_date - start_date).days)):
            # Skip weekends
            if day.weekday() in (5, 6):
                continue

            # Add new slots for this date
            time_slots = [f"{hour:02d}:{minute:02d}" for hour in range(9, 17) for minute in (0, 30)]
            for slot in time_slots:
                cursor.execute("""
                    INSERT INTO appointments (date, time_slot, gp_email, patient_email, appointment_status)
                    VALUES (?, ?, ?, NULL, "Available")
                """, (str(day), slot, gp_email))
        print(f"Time slots populated for {gp_email} from {start_date} to {end_date}.")

    # Commit changes and close the connection
    connection.commit()
    connection.close()
def confirm_appointments(gp_email):

    conn = sqlite3.connect('appointments.db')
    cursor = conn.cursor()

    query = """
    SELECT id, date, time_slot, patient_email
    FROM appointments
    WHERE gp_email = ? AND appointment_status = 'Requested'
    ORDER BY date, time_slot;
    """
    cursor.execute(query, (gp_email,))
    rows = cursor.fetchall()

    if not rows:
        print("No requested appointments to confirm.\nReturning to Main menu...")
        conn.close()
        gp_page(gp_email)

    table = []
    headers = ["Slot ID", "Date", "Time Slot", "Patient Email"]

    for row in rows:
        table.append(row)

    print("\nRequested Appointments:")
    print(tabulate.tabulate(table, headers=headers, tablefmt='grid'))

    # Allow GP to confirm appointments
    valid_ids = {row[0] for row in rows}  # Set of valid Slot IDs
    while True:
        confirm = input("\nEnter [Slot ID] to confirm (or 'Q' to quit): ").strip()
        if confirm.upper() == 'Q':
            conn.close()
            print("\nReturning to Main menu...")
            sleep(2)
            gp_page(gp_email)
        else:
            try:
                slot_id = int(confirm)
                if slot_id in valid_ids:
                    cursor.execute("""
                    UPDATE appointments
                    SET appointment_status = 'Confirmed'
                    WHERE id = ? AND gp_email = ?;
                    """, (slot_id, gp_email))
                    conn.commit()
                    print(f"Appointment [{slot_id}] confirmed.")
                    # Remove the confirmed ID from valid_ids to avoid re-confirming it
                    valid_ids.remove(slot_id)
                else:
                    print("Invalid Slot ID. Please choose a valid [Slot ID] from the table.")
            except ValueError:
                print("Invalid input. Please enter a valid [Slot ID].")
def view_upcoming_appointments(gp_email):

    conn = sqlite3.connect('appointments.db')
    cursor = conn.cursor()

    # Query to fetch upcoming confirmed and requested appointments for the GP
    query = """
    SELECT id, date, time_slot, patient_email, appointment_status
    FROM appointments
    WHERE gp_email = ? AND appointment_status IN ('Confirmed', 'Requested') AND date >= ?
    ORDER BY date, time_slot;
    """
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute(query, (gp_email, today))
    rows = cursor.fetchall()

    if not rows:
        print("No upcoming appointments found.\nReturning to Main menu...")
        conn.close()
        sleep(2)
        gp_page(gp_email)

    # Display confirmed and requested appointments in a table
    table = []
    headers = ["Slot ID", "Date", "Time Slot", "Patient Email", "Status"]

    for row in rows:
        table.append(row)

    print("\nUpcoming Appointments (Confirmed and Requested):")
    print(tabulate.tabulate(table, headers=headers, tablefmt='grid'))
    conn.close()

    print(f"\n")
    print("[ 1 ] Confirm appointments")
    print("[ 2 ] Cancel appointments")
    print("[ M ] Return to Main menu")
    while True:
        c5 = input("Please select an option: ")
        if c5.upper() == "M":
            gp_page(gp_email)
        elif c5 == "1":
            confirm_appointments(gp_email)
        elif c5 == "2":
            cancel_gp_appointment(gp_email)
        else:
            print("Please choose a valid option '1' , '2' or 'M'")
def cancel_gp_appointment(gp_email):

    conn = sqlite3.connect('appointments.db')
    cursor = conn.cursor()

    query = """
    SELECT id, date, time_slot, patient_email, appointment_status
    FROM appointments
    WHERE gp_email = ? AND patient_email IS NOT NULL
    ORDER BY date, time_slot;
    """
    cursor.execute(query, (gp_email,))
    rows = cursor.fetchall()

    if not rows:
        print("No booked appointments found to cancel.\nReturning to Main menu...")
        conn.close()
        sleep(2)
        gp_page(gp_email)

    # Display appointments in a table
    table = []
    headers = ["Slot ID", "Date", "Time Slot", "Patient Email", "Status"]

    for row in rows:
        table.append(row)

    print("\nBooked Appointments (Requested or Confirmed):")
    print(tabulate.tabulate(table, headers=headers, tablefmt='grid'))

    # Allow GP to select an appointment to cancel
    valid_ids = {row[0] for row in rows}  # Set of valid Slot IDs
    while True:
        cancel = input("\nEnter [Slot ID] to cancel (or 'Q' to quit): ").strip()
        if cancel.upper() == 'Q':
            print("\nReturning to Main menu...")
            conn.close()
            sleep(2)
            gp_page(gp_email)

        try:
            slot_id = int(cancel)
            if slot_id in valid_ids:
                confirm = input(f"Are you sure you want to cancel appointment [{slot_id}]? (y/n): ").strip().lower()
                if confirm == 'y':
                    cursor.execute("""
                    UPDATE appointments
                    SET patient_email = NULL, appointment_status = 'Available'
                    WHERE id = ? AND gp_email = ?;
                    """, (slot_id, gp_email))
                    conn.commit()
                    print(f"Appointment [{slot_id}] has been canceled.")
                    valid_ids.remove(slot_id)
                else:
                    print("Cancellation aborted.")
            else:
                print("Invalid Slot ID. Please choose a valid Slot ID from the table.")
        except ValueError:
            print("Invalid input. Please enter a valid Slot ID.")

# [ 3 ] Manage patient records
def view_patient_summary(gp_email):
    print("=" * 80)
    print("VIEW PATIENT SUMMARY".center(80))
    print("\nEnter 'M' to return to the main menu\n")

    # Load patient data
    data = load_accounts()
    patients = data.get("patient", {})

    # Display list of patients
    patient_list = []
    for idx, (email, details) in enumerate(patients.items(), start=1):
        patient_list.append({
            "Index": idx,
            "Email": email,
            "Name": details.get("name", "Unknown"),
            "Surname": details.get("surname", "Unknown"),
            "Date of Birth": details.get("date_of_birth", "Unknown")
        })
    df_patients = pandas.DataFrame(patient_list)
    print("List of Patients:")
    print(tabulate.tabulate(df_patients, headers='keys', tablefmt='grid', showindex=False))

    # Select a patient
    while True:
        selection = input("\nEnter the Index of the patient to view summary or 'M' to return: ").strip()
        if selection.upper() == "M":
            manage_patient_information(gp_email)
            return
        try:
            selection = int(selection)
            if 1 <= selection <= len(patient_list):
                selected_patient = patient_list[selection - 1]
                patient_email = selected_patient["Email"]
                break
            else:
                print("Invalid selection. Please enter a valid Index.")
        except ValueError:
            print("Invalid input. Please enter a number corresponding to a patient.")

    patient_details = patients[patient_email]
    summary_data = {
        "Full Name": f"{patient_details.get('name', 'Unknown')} {patient_details.get('surname', 'Unknown')}",
        "Date of Birth": patient_details.get("date_of_birth", "Unknown"),
        "Gender": patient_details.get("gender", "Unknown"),
        "Email": patient_email,
        "Address Line 1": patient_details.get("Address_Line_1", "Unknown"),
        "Address Line 2": patient_details.get("Address_Line_2", "Unknown"),
        "NHS Organ Donor Status": patient_details.get("NHS_organ_donor", "Unknown"),
        "NHS Blood Donor Status": patient_details.get("NHS_blood_donor", "Unknown")
    }

    # Reshape data to have two columns: Field and Value
    df_summary = pandas.DataFrame(list(summary_data.items()), columns=["Field", "Value"])

    print("\nPatient Summary:")
    print(tabulate.tabulate(df_summary, headers='keys', tablefmt='grid', showindex=False))

    input("\nPress Enter to return to Manage Patient Information.")
    manage_patient_information(gp_email)
def view_patient_journals(gp_email):
    print("=" * 80)
    print("VIEW PATIENT JOURNALS".center(80))
    print("\nEnter 'M' to return to the main menu\n")

    # Load patient data
    data = load_accounts()
    patients = data.get("patient", {})

    # Display list of patients
    patient_list = []
    for idx, (email, details) in enumerate(patients.items(), start=1):
        patient_list.append({
            "Index": idx,
            "Email": email,
            "Name": details.get("name", "Unknown"),
            "Surname": details.get("surname", "Unknown"),
            "Date of Birth": details.get("date_of_birth", "Unknown")
        })
    df_patients = pandas.DataFrame(patient_list)
    print("List of Patients:")
    print(tabulate.tabulate(df_patients, headers='keys', tablefmt='grid', showindex=False))

    # Select a patient
    while True:
        selection = input("\nEnter the Index of the patient to view journals or 'M' to return: ").strip()
        if selection.upper() == "M":
            manage_patient_information(gp_email)
            return
        try:
            selection = int(selection)
            if 1 <= selection <= len(patient_list):
                selected_patient = patient_list[selection - 1]
                patient_email = selected_patient["Email"]
                break
            else:
                print("Invalid selection. Please enter a valid Index.")
        except ValueError:
            print("Invalid input. Please enter a number corresponding to a patient.")

    # Display patient's journals
    patient_details = patients[patient_email]
    journals = patient_details.get("journals", [])

    if not journals:
        print("\nNo journal entries found for this patient.")
    else:
        # Convert journals to DataFrame
        df_journals = pandas.DataFrame(journals)
        print("\nPatient Journals:")
        print(tabulate.tabulate(df_journals, headers='keys', tablefmt='grid', showindex=False))

    input("\nPress Enter to return to Manage Patient Information.")
    manage_patient_information(gp_email)
def view_patient_records(gp_email):
    print("=" * 80)
    print("VIEW PATIENT RECORDS".center(80))
    print("\nEnter 'M' to return to the main menu\n")

    # Load patient data
    data = load_accounts()
    patients = data.get("patient", {})

    # Display list of patients
    patient_list = []
    for idx, (email, details) in enumerate(patients.items(), start=1):
        patient_list.append({
            "Index": idx,
            "Email": email,
            "Name": details.get("name", "Unknown"),
            "Surname": details.get("surname", "Unknown"),
            "Date of Birth": details.get("date_of_birth", "Unknown")
        })
    df_patients = pandas.DataFrame(patient_list)
    print("List of Patients:")
    print(tabulate.tabulate(df_patients, headers='keys', tablefmt='grid', showindex=False))

    # Select a patient
    while True:
        selection = input("\nEnter the Index of the patient to view records or 'M' to return: ").strip()
        if selection.upper() == "M":
            manage_patient_information(gp_email)
            return
        try:
            selection = int(selection)
            if 1 <= selection <= len(patient_list):
                selected_patient = patient_list[selection - 1]
                patient_email = selected_patient["Email"]
                break
            else:
                print("Invalid selection. Please enter a valid Index.")
        except ValueError:
            print("Invalid input. Please enter a number corresponding to a patient.")

    # Display patient's conditions
    patient_details = patients[patient_email]
    conditions = patient_details.get("conditions", [])
    clinical_notes = patient_details.get("clinical_notes", [])

    if not isinstance(clinical_notes, list):
        clinical_notes = [{"date": "Unknown", "note": clinical_notes}]  # Backward compatibility

    # Create DataFrame for conditions
    df_conditions = pandas.DataFrame({"Conditions": conditions})
    print("\nPatient Conditions:")
    print(tabulate.tabulate(df_conditions, headers='keys', tablefmt='grid', showindex=False))

    # Display clinical notes in tabular format
    df_notes = pandas.DataFrame(clinical_notes)
    print("\nClinical Notes:")
    if not df_notes.empty:
        print(tabulate.tabulate(df_notes, headers=['Date', 'Note'], tablefmt='grid', showindex=False))
    else:
        print("No clinical notes available.")

    # Options to add or edit conditions and clinical notes
    while True:
        print("\nOptions:")
        print("[ 1 ] Add condition")
        print("[ 2 ] Edit conditions")
        print("[ 3 ] Add clinical note")
        print("[ M ] Return to Manage Patient Information")
        choice = input("Select an option: ").strip().upper()
        if choice == "1":
            # Code to add condition
            conditions_list = ["Anxiety", "Depression", "Autism", "PTSD", "Bipolar Disorder"]
            print("\nAvailable Mental Conditions:")
            for i, condition in enumerate(conditions_list, 1):
                print(f"[ {i} ] {condition}")
            print("[ 0 ] Custom condition")
            selected_conditions = ""
            while True:
                choice_c = input("Select a condition by number (or press Enter to cancel): ").strip()
                if choice_c == "":
                    break
                elif choice_c == "0":
                    custom_condition = input("Enter a custom condition: ").strip()
                    if custom_condition:
                        selected_conditions = custom_condition
                elif choice_c.isdigit() and 1 <= int(choice_c) <= len(conditions_list):
                    selected_conditions = conditions_list[int(choice_c) - 1]
                    break
                else:
                    print("Invalid choice. Try again.")

            if selected_conditions:
                conditions.append(selected_conditions)
                patient_details["conditions"] = conditions
                save_accounts(data)
                print("Condition added successfully.")
            else:
                print("No condition entered.")
        elif choice == "2":
            # Code to edit conditions
            if not conditions:
                print("No conditions to edit.")
                continue
            print("\nCurrent Conditions:")
            for idx, cond in enumerate(conditions, start=1):
                print(f"[ {idx} ] {cond}")
            cond_idx = input("Enter the number of the condition to edit: ").strip()
            try:
                cond_idx = int(cond_idx)
                if 1 <= cond_idx <= len(conditions):
                    new_value = input("Enter the replacement for the condition (or R to remove this condition): ").strip()
                    if new_value.upper() == "R":
                        del conditions[cond_idx - 1]
                        patient_details["conditions"] = conditions
                        save_accounts(data)
                        print("Conditions list updated successfully.")
                    elif new_value:
                        conditions[cond_idx - 1] = new_value
                        patient_details["conditions"] = conditions
                        save_accounts(data)
                        print("Conditions list updated successfully.")
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid input.")
        elif choice == "3":
            # Code to add clinical notes
            new_note = input("Enter new clinical note: ").strip()
            if new_note:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                clinical_notes.append({"date": timestamp, "note": new_note})
                patient_details["clinical_notes"] = clinical_notes
                save_accounts(data)
                print("Clinical note added successfully.")
            else:
                print("No note entered.")
        elif choice == "M":
            manage_patient_information(gp_email)
            return
        else:
            print("Invalid choice. Please select a valid option.")
def manage_patient_information(gp_email):
    print("=" * 80)
    print("MANAGE PATIENT INFORMATION".center(80))
    print("[ 1 ] View patient records")
    print("[ 2 ] View patient journals")
    print("[ 3 ] View patient summary")
    print("[ M ] Return to main menu")

    while True:
        choice = input("\nPlease select an option: ").strip().upper()
        if choice == "1":
            view_patient_records(gp_email)
        elif choice == "2":
            view_patient_journals(gp_email)
        elif choice == "3":
            view_patient_summary(gp_email)
        elif choice == "M":
            gp_page(gp_email)
            break
        else:
            print("Invalid choice. Please select '1', '2', '3', or 'M'.")

# [ 4 ] Check in/out patients
#==========================================================


#====================Homepage Accounts=====================
def patients_page(email_address):
    print("=" * 80)
    print("PATIENT HOMEPAGE".center(80))
    print(termcolor.colored("Welcome, Patient. Ready to take the next step in your well-being journey?".center(80), "green"))
    print("-" * 80)
    print("[ 1 ] Book and manage appointments")
    print("[ 2 ] Change default GP")
    print("[ 3 ] Access meditation help & tips and more")
    print("[ 4 ] Access journal entries")
    print("[ 5 ] Change account details")
    print("[ 6 ] Helplines")
    print("[ X ] Logout")

    while True:
        choice = input("\nPlease select an option: ").strip()
        if choice.upper() == "X":
            login_menu()
        elif choice == "1":
            book_and_manage_appointments(email_address)
        elif choice == "2":
            print("FUNCTION NOT ADDED. WORK IN PROGRESS")   #<---------------------------Put function here.
            main_menu()
        elif choice == "3":
            mhresources(email_address)
        elif choice == "4":
            journal_page(email_address)
        elif choice == "5":
            update_account_page(email_address)
        elif choice == "6":
            helplines(email_address)
        else:
            print("Please choose a valid option '1' , '2', '3', '4', '5', '6' or 'X'")
def gp_page(gp_email):
    print("=" * 80)
    print("GP HOMEPAGE".center(80))
    print(termcolor.colored("Welcome, GP. Your dedication helps patients achieve their best mental health.".center(80), "green"))
    print("[ 1 ] View schedule")
    print("[ 2 ] Manage appointments ")
    print("[ 3 ] Manage patient records")
    print("[ 4 ] Check in/out patients ")
    print("[ 5 ] Change patient details ")
    print("[ X ] Logout")

    while True:
        choice1 = input("\nPlease select and option: ").strip()
        if choice1.upper() == "X":
            login_menu()
        elif choice1 == "1":
            view_gp_schedule(gp_email)
        elif choice1 == "2":
            manage_appointments(gp_email)
        elif choice1 == "3":
            manage_patient_information(gp_email)
        elif choice1 == "4":
            print("FUNCTION NOT ADDED. WORK IN PROGRESS")   #<---------------------------Put function here.
            main_menu()
        elif choice1 == "5":
            print("FUNCTION NOT ADDED. WORK IN PROGRESS")   #<---------------------------Put function here.
            main_menu()
        else:
            print("Please choose a valid option '1' , '2', '3', '4', '5' or 'X'")
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
            manage_gp_system()

        elif choice == "2":
            delete_accounts()

        elif choice == "3":
            manage_gp_details()

        elif choice == "4":
            manage_accounts()

        elif choice == "5":
            display_summary_info_system()

        else:
            print("Please choose a valid option '1' , '2', '3', '4', '5' or 'X'")
#==========================================================


#=================Registration Functions===================
def verify_credentials(email, v_password, role):
    role_accounts = registered_users[role]
    if email in role_accounts:
        if role_accounts[email]["password"] == v_password:
            return True
        else:
            return "Incorrect password"
    else:
        return "Email not found"
def checking_email(email):
    email = email.lower()
    for role_accounts in registered_users.values():
        if email in map(str.lower, role_accounts.keys()):  # Ensure case-insensitive comparison
            return "Email already registered"
    return "Email available"
def registering_user():
    print("=" * 80)
    print("REGISTERING".center(80))
    print("Please enter your details \n\nEnter 'M' to return to main menu\n")
    first_name = input("First name: ").strip()
    if first_name.upper() == "M":
        main_menu()
    sur_name = input("Last name: ").strip()
    if sur_name.upper() == "M":
        main_menu()

    while True:
        date_input = input("Birth date (DD/MM/YYYY): ").strip()  # Pad single digit day with zero if necessary
        if date_input.upper() == "M":
            main_menu()
        else:
            try:
                date_input.zfill(2)
                day, month, year = date_input.split("/")
                day = int(day)
                month = int(month)
                year = int(year)
            except Exception:
                print(f"Invalid birth date, try again.")
                continue

            try:
                if not (1 <= day <= 31):
                    print("Invalid day. Please enter a day between 01 and 31.")
                elif not (1 <= month <= 12):
                    print("Invalid month. Please enter a month between 01 and 12.")
                elif not (1900 <= year <= datetime.now().year):
                    print(f"Invalid year. Please enter a year between 1900 and {datetime.now().year}.")
                else:
                    datetime.strptime(date_input, "%d/%m/%Y")
                    break
            except Exception:
                print(f"Invalid birth date, try again.")



    while True:
        role = input("Are you a Patient or GP? : ").strip()
        if role.upper() == "M":
            main_menu()
        role = role.replace(" ", "").strip().lower()
        if role == "patient":
            break
        elif role == "gp":
            break
        else:
            print(f"The role '{role}' does not exist. Try entering Patient or GP.")


    while True:
        email_address = input("Email address: ").strip()
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.[\w\.-]+$"
        if email_address.upper() == "M":
            main_menu()
        email_check = checking_email(email_address)

        if email_check == "Email already registered":
            print("This email is already registered. Please use a different email.")
        else:
            if match(email_pattern, email_address):
                break
            elif not match(email_pattern, email_address):
                print("Invalid email format. Please enter a valid email.")
            else:
                print("Invalid email format. Please enter a valid email.")
                print("Press 'M' to return to main menu")


    while True:
        input_password = input("Password [8 characters min, 1 uppercase letter min, and 1 number min]: ").strip()
        if input_password.upper() == "M":
            main_menu()

        has_upper = False
        has_digit = False
        password_pattern = r'^(?=.*[A-Z])(?=.*\d)[A-Za-z\d!@#$%^&*()_+{}|:<>?~]{8,}$'

        for char in input_password:
            if char.isupper():
                has_upper = True
            if char.isdigit():
                has_digit = True
            if has_upper and has_digit:
                break

        if not has_upper:
            print("The password is missing an uppercase letter.")
        elif not has_digit:
            print("The password is missing a number.")
        elif len(input_password) < 8:
            print ("Password length is less than 8 characters.")
        elif not match(password_pattern, input_password):
            print ("Password is weak, try a stronger password")
        else:
            confirm_password = input("Confirm password: ")
            if confirm_password != input_password:
                print("Passwords do not match, please enter password again")
            else:
                break

    while True:
        print ("Genders:")
        print ("[ 1 ] Male")
        print ("[ 2 ] Female")

        try:
            user_gender = input("Please choose an option: ").strip()
            if user_gender.upper() == "M":
                main_menu()

            if user_gender == "1":
                user_gender = "Male"
                break
            elif user_gender == "2":
                user_gender = "Female"
                break
            else:
                print ("Please choose a valid option '1' or '2' ")
        except Exception:
            print("Invalid option")

    if role == "patient":
        while True:
            print ("NHS blood donor:")
            print ("[ 1 ] Yes")
            print ("[ 2 } No")

            try:
                a = input("Please choose an option: ").strip()
                if a.upper() == "M":
                    main_menu()

                if a == "1":
                    a = "IS Blood donor"
                    break
                elif a=="2":
                    a = "NOT Blood donor"
                    break
                else:
                    print ("Please choose '1', '2' or 'M' to return to menu")
            except Exception:
                print("Invalid option")

        while True:
            print ("NHS organ donor:")
            print ("[ 1 ] Yes")
            print ("[ 2 } No")

            try:
                b = input("Please choose an option: ").strip()
                if b.upper() == "M":
                    main_menu()

                if b == "1":
                    b = "IS Organ donor"
                    break
                elif b=="2":
                    b = "NOT Organ donor"
                    break
                else:
                    print ("Please choose '1', '2' or 'M' to return to menu")
            except Exception:
                print("Invalid option")

    while True:
        try:
            ad1 = input("Address Line 1 (House number, street name): ")
            if ad1.upper() == "M":
                main_menu()
            address_line_1_pattern = r"^\d+\s+[\w\s\-']+(\s+(Apt|Suite|St|Rd|Lane|Blvd|Ave|Dr|Court|Pl|Road|Street|Way|Close))?(\s*\d*[A-Za-z]?)?$"

            if match(address_line_1_pattern, ad1):
                break
            else:
                print("Address Line 1 is not valid.")
        except Exception:
            print("Invalid address, try again")

    while True:
        try:
            ad2 = input("Address Line 2 (Postcode, zipcode, or country): ")
            if ad2.upper() == "M":
                main_menu()
            address_line_2_pattern = r'^[A-Za-z0-9\s,]+$'

            if match(address_line_2_pattern, ad2):
                break
            else:
                print("Address Line 1 is not valid.")
        except Exception:
            print("Invalid address, try again")

    if role == "patient":
        user = Accounts(email_address, input_password, first_name, sur_name,
                               date_input, user_gender, role, a, b, ad1, ad2)
    elif role == "gp":
        user = Accounts(email_address, input_password, first_name, sur_name,
                               date_input, user_gender, role, ad1, ad2)


    print("Your account has been made.")
    print("Current account is being registered to system...")
    sleep(3)
    print("Returing to main menu.")
    sleep(1)
class Accounts:
    def __init__(self, email, a_password, name, surname, date_of_birth, gender,
                 job_role, nhs_blood_donor=None, nhs_organ_donor=None, address_line_1="Unknown", address_line_2="Unknown",
                 conditions=None):
        self.email = email
        self.password = a_password
        self.name = name
        self.surname = surname
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.job_role = job_role
        self.NHS_blood_donor = nhs_blood_donor or "Unknown"
        self.NHS_organ_donor = nhs_organ_donor or "Unknown"
        self.Address_Line_1 = address_line_1
        self.Address_Line_2 = address_line_2
        self.journals = []
        self.conditions = conditions if conditions is not None else []

        self.add_to_role_accounts()

    def add_to_role_accounts(self):
        user_details = {
            "email": self.email,
            "password": self.password,
            "name": self.name or "Unknown",
            "surname": self.surname or "Unknown",
            "date_of_birth": self.date_of_birth or "Unknown",
            "gender": self.gender or "Unknown",
            "NHS_blood_donor": self.NHS_blood_donor or "Unknown",
            "NHS_organ_donor": self.NHS_organ_donor or "Unknown",
            "Address_Line_1": self.Address_Line_1 or "Unknown",
            "Address_Line_2": self.Address_Line_2 or "Unknown",
            "journals": [],
            "conditions": [],
            "clinical_notes": "None"
        }

        # Add to the appropriate role in registered_users
        if self.job_role in registered_users:
            registered_users[self.job_role][self.email] = user_details
        else:
            # If the role does not exist, create it
            registered_users[self.job_role] = {self.email: user_details}

        # Save the updated registered_users dictionary to the JSON file
        save_accounts(registered_users)
#==========================================================


#==================Login Function==========================
def reset_password():
    print("=" * 80)
    print("PASSWORD RESET".center(80))
    print("\nEnter 'M' to return to main menu\n")
    count = 10

    while count > 0:
        email_addresss = input("Enter your registered email address: ")
        if email_addresss.upper() == "M":
            main_menu()
            return

        roless = None
        for role_type, accounts in registered_users.items():
            if email_addresss in accounts:
                roless = role_type
                break

        if roless:
            break
        else:
            print("Email not found.")
            count -= 1
            if count == 0:
                print("Too incorrect tries. Returing to main menu")
                main_menu()
                return

    reset_code = str(randint(100000, 999999))
    print(f"Simulated reset code sent to {email_addresss}: {reset_code}")  # In real application, send to email

    for attempt in range(4):
        user_code = input("Enter the reset code sent to your email: ")
        if user_code == reset_code:
            break
        elif user_code.upper() == "M":
            main_menu()
            return
        else:
            print("Incorrect code.")
            if attempt == 3:
                print("Too many incorrect attempts. Returning to main menu.")
                main_menu()
                return
    else:
        main_menu()
        return

    tries = 4
    while tries > 0:
        new_password = input("Please enter new password [8 characters min, 1 uppercase letter min, and 1 number min]: ")
        if new_password.upper() == "M":
            main_menu()
            return

        password_pattern = r'^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'

        if new_password == registered_users[roless][email_addresss]["password"]:
            print("New password cannot be same as previous password")
            tries -= 1
        elif not match(password_pattern, new_password):
            print("Password is weak, try a stronger password")
            tries -= 1
        elif tries == 1:
            print("Too many incorrect inputs. Returning to main menu")
        elif match(password_pattern, new_password):
            confirm_password = input("Confirm password: ")
            if confirm_password != new_password:
                print("Passwords do not match, please enter password again")
            else:
                break
        else:
            break


    registered_users[roless][email_addresss]["password"] = new_password
    save_accounts(registered_users)
    print("Password reset successfully.")
    main_menu()
    return
def login_user(role):
    print("-" * 80)
    print("Please enter your details \n\nEnter 'R' to return to reset password\nEnter 'M' to return to main menu\n")

    login_attempts = 10
    while login_attempts > 0:
        email_address = input("Email address: ").strip().lower()
        if email_address.upper() == "R":
            reset_password()
        elif email_address.upper() == "M":
            main_menu()

        email_found = False
        for role_type, accounts in registered_users.items():
            if email_address in accounts:
                email_found = True
                break

        if not email_found:
            print(f"Email not found in {role.capitalize()} database. Please try again.")
            login_attempts -= 1
            if login_attempts == 0:
                print("Too many incorrect attempts. Returning to main menu.")
                sleep(2)
                main_menu()
            continue

        password_attempts = 4
        while password_attempts > 0:
            login_password = input("Password: ")
            if login_password.upper() == "R":
                reset_password()
            elif login_password.upper() == "M":
                main_menu()


            if email_address in map(str.lower, registered_users["admin"]) and \
                    registered_users["admin"][email_address]["password"] == login_password:
                print("Admin login successful")
                admins_page()


            result = verify_credentials(email_address, login_password, role=role)

            if result == True:
                print(f"{role.capitalize()} login successful")
                if role == "patient":
                    patients_page(email_address=email_address)
                elif role == "gp":
                    gp_page(email_address)
                elif role == "admin":
                    admins_page()
                return

            elif result == "Incorrect password":
                password_attempts -= 1
                if password_attempts == 0:
                    print("\nToo many incorrect attempts. Returning to main menu.")
                    sleep(2)
                    main_menu()
                print(f"\nEmail found in database. Incorrect password. You have {password_attempts} attempt(s) left.")

        print("Returning to email input due to too many incorrect password attempts.")
        break
def login_menu():
    while True:
        print("=" * 80)
        print("LOGIN AS:".center(80))
        print("[ 1 ] Patient")
        print("[ 2 ] GP")
        print("[ 3 ] Admin")
        print("[ M ] Main menu")
        print("[ E ] Exit")

        user = input("Please choose an option: ").strip()
        if user == "1":
            login_user("patient")
        elif user == "2":
            login_user("gp")
        elif user == "3":
            login_user("admin")
        elif user.upper() == "E":
            print("=" * 80)
            print("Exiting!")
            # uninstall_modules()
            exit()
        elif user.upper() == "M":
            main_menu()
        else:
            print("Invalid choice! Please enter 1, 2, 3, E, or M.")
#=========================================================


#=======================Main menu=========================
def main_menu():
    while True:
        print("=" * 80)
        print("UCL Management System".center(80))
        print("[ 1 ] Login")
        print("[ 2 ] Register")
        print("[ E ] Exit")

        choice = input("Please choose an option: ").strip()
        if choice == "1":
            login_menu()
        elif choice == "2":
            registering_user()
        elif choice.upper() == "E":
            print("=" * 80)
            print("EXITING!".center(80))
            # uninstall_modules()
            # Accounts.display_all_accounts()
            exit()
        else:
            print("Invalid choice! Please enter 1, 2, or E.")
#=========================================================


#====================Call function========================
def call_function():
    ensure_pip_installed()
    install_modules()
    initialize_database()
    initialize_and_populate_new_gp_slots()
    update_time_slots()
    header()
    main_menu()

call_function()
#=========================================================