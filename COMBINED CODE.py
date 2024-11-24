import re
#=======================Modules=============================
from importlib import import_module
from time import sleep
from sys import exit, executable
from re import match
from random import randint
from datetime import datetime
from json import load, dump, JSONDecodeError
from platform import system
import os
import subprocess


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

#other functions...
#==========================================================


#====================Patient Homepage======================

#[ 1 ] Book and manage appointments
#[ 2 ] Change default GP
#[ 3 ] Access meditation help & tips and more
#[ 4 ] Change account details
#[ X ] Logout
# Dictionary containing resources for different categories
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
        print("Type 'exit' to return to the patient homepage.")

        user_input = input("Enter the number corresponding to the category: ").strip().lower()

        if user_input == "exit":
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
    print("Type 'back' to return to the main menu.")

    while True:
        user_input = input("Enter the number corresponding to the resource: ").strip().lower()

        if user_input == "back":
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
    print("Type 'back' to return to the patient homepage, if further support is needed.")

    while True:
        user_input = input("Enter the number corresponding to your choice or type 'back': ").strip().lower()

        if user_input == "1":
            return category_menu(category_name)
        elif user_input == "2":
            mhresources(email_address=email_address)
        elif user_input == "back":
            patients_page(email_address=email_address)
        else:
            print("Invalid input. Please enter a valid option.")


def update_account_page(email_address):
    data = load_accounts()
    account_details = data["patient"][email_address]
    updates_made = False

    while True:
        print("--------------------------------------------------------------------------------")
        print("These are your current account details:\n")
        counter = 1
        for key, value in account_details.items():
            if key != "password" and key!= "journals" and key!= "conditions" and key!= "clinical_notes" :
                print("[", counter, "] ", (key[0].upper()) + key[1:len(key)].replace("_", " "), ": ", value)
                counter += 1
        print("[ 0 ]  Exit to Homepage ")
        print("\n")


        update_option = input("Please select an option to edit: ").strip()
        if (update_option.isdigit() and 0 <= int(update_option) <= 9) :
            update_option = int(update_option)
        else:
            print("\n")
            print("Invalid input. Please choose a valid option")
            continue


        if update_option == 0:
            print("Returning to your homepage...")
            sleep(1)
            patients_page(email_address)
            break


        if update_option == 1:
            while True:
                new_email = input("Please enter your new email address:").strip()
                email_pattern = r"^[\w\.-]+@[\w\.-]+\.[\w\.-]+$"

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
                                print("Too many incorrect attempts. No change has been made to your account. Returning to your homepage...")
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
                    final_confirmation = input("Please confirm you would like to make this change to your account (Y/N) ").strip().lower()
                    if final_confirmation == "y":
                        account_details["name"] = new_first_name
                        updates_made = True
                        break

                    elif final_confirmation == "n":
                        print("Returning to your patient homepage...")
                        sleep(1)
                        patients_page(email_address)

                    else:
                        print("Please input a valid option, either Y or N ")

            else:
                print("This is already your current first name")



        elif update_option == 3:
            new_surname = input("Please enter your new surname").strip()
            if new_surname != account_details["surname"]:
                while True:
                    final_confirmation = input("Please confirm you would like to make this change to your account (Y/N) ").strip().lower()
                    if final_confirmation == "y":
                        account_details["surname"] = new_surname
                        updates_made = True
                        break

                    elif final_confirmation == "n":
                        print("Returning to your patient homepage...")
                        sleep(1)
                        patients_page(email_address)

                    else:
                        print("Please input a valid option, either Y or N ")

            else:
                print("This is already your current surname")


        elif update_option == 4:
            while True:
                new_birthday = input("Birth date (DD/MM/YYYY): ").strip()  # Pad single digit day with zero if necessary
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
                    print("This is already your current date of birth")
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
                print("NHS blood donor:")
                print("[ 1 ] Yes")
                print("[ 2 } No")
                donor_new = input("Please choose an option: ").strip()
                if donor_new == "1":
                    donor_new = "IS Blood donor"
                elif donor_new == "2":
                    donor_new = "NOT Blood donor"
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

            ad1_new = input("Please enter a new Address Line 1 ")
            if ad1_new != account_details["Address_Line_1"]:
                while True:
                    final_confirmation = input("Please confirm you would like to make this change to your account (Y/N) ").strip().lower()
                    if final_confirmation == "y":
                        account_details["Address_Line_1"] = ad1_new
                        updates_made = True
                        break

                    elif final_confirmation == "n":
                        print("Returning to your patient homepage...")
                        sleep(1)
                        patients_page(email_address)

                    else:
                        print("Please input a valid option, either Y or N ")

            else:
                print("This is already your current Address Line 2")


        elif update_option == 9:
            ad2_new = input("Please enter a new Address Line 2 ")
            if ad2_new != account_details["Address_Line_2"]:
                while True:
                    final_confirmation = input("Please confirm you would like to make this change to your account (Y/N) ").strip().lower()
                    if final_confirmation == "y":
                        account_details["Address_Line_2"] = ad2_new
                        updates_made = True
                        break

                    elif final_confirmation == "n":
                        print("Returning to your patient homepage...")
                        sleep(1)
                        patients_page(email_address)

                    else:
                        print("Please input a valid option, either Y or N ")
            else:
                print("This is already your current Address Line 2")

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
            print("No changes were made.")
            sleep(1)

        print("--------------------------------------------------------------------------------")
        print("Updated account details:")
        print("")
        for key,value in account_details.items():
            if key != "password" and key!= "journals" and key!= "conditions" and key!= "clinical_notes" :
                print((key[0].upper()) + key[1:len(key)].replace("_", " "), ": ", value)

        print("\n")
        edit_again= input("Would you like to eit another detail? (Y/N): ").strip().lower()
        if edit_again == "n":
            print("Returning to your homepage...")
            sleep(1)
            patients_page(email_address)
            break
        elif edit_again!= "y":
            print("Invalid input, returning to the edit menu")




def journal_page(email_address):
    while True:
        print("="* 80)
        print("JOURNALS PAGE".center(80))
        print("[ 1 ] View previous entries")
        print("[ 2 ] Make a new journal entry")
        print("[ H ] Return to your homepage")
        choice= input("\nPlease select an option: ").strip().upper()
        if choice == "1":
            view_journal_entries(email_address)
        elif choice == "2":
            new_journal_entry(email_address)
        elif choice == "H":
            print("Returning to your homepage...")
            sleep(1)
            patients_page(email_address)
            break
        else:
            print("Invalid choice, please select '1', '2' or 'H' ")




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
    data=load_accounts()
    patient_account= data["patient"][email_address]
    journals = patient_account.get("journals", [] )
    if not journals:
        print("\nYou have no journal entries. ")
        return
    journals_sorted = sorted(journals, key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d %H:%M:%S"))

    print("\nYour Journal Entries:")
    for idx, journal in enumerate(journals_sorted, start=1):
        print(f"\nEntry {idx} - Date: {journal['date']}")
        print("-" * 40)
        print(journal['entry'])
        print("-" * 40)



#==========================================================


#=======================GP Homepage========================
# [ 1 ] View schedule
# [ 2 ] Manage appointments
# [ 3 ] Manage patient records
ACCOUNTS_FILE = "accounts.json"
MEDICAL_RECORDS_FILE = "medical_records.json"

# Function to load the accounts from the accounts.json file
def load_accounts2():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as file:
            try:
                return load(file)  # Load existing account data
            except JSONDecodeError:
                return {}  # Return empty dictionary if JSON is corrupted or empty
    else:
        return {}  # Return empty dictionary if the file doesn't exist

# Function to load or initialize medical records
def load_or_initialize_records():
    if os.path.exists(MEDICAL_RECORDS_FILE):
        with open(MEDICAL_RECORDS_FILE, "r") as file:
            try:
                # Try loading existing medical records
                return load(file)
            except JSONDecodeError:
                # If the file is empty or corrupted, initialize it
                accounts = load_accounts2()
                data_default = {"note": "", "date_created": None}
                records = {}  # Create a dictionary for the medical records

                # Populate medical records for patients only
                for role, account_data in accounts.items():
                    if role == "patient":
                        for email in account_data.keys():
                            records[email] = [data_default]

                # Write the initialized records to the file
                with open(MEDICAL_RECORDS_FILE, "w") as file_1:
                    dump(records, file_1, indent=4)

                return records  # Return the newly created records
    else:
        # If the file doesn't exist, initialize a new file
        accounts = load_accounts2()
        data_default = {"note": "", "date_created": None}
        records = {}

        # Populate medical records for patients only
        for role, account_data in accounts.items():
            if role == "patient":
                for email in account_data.keys():
                    records[email] = [data_default]

        # Write to a new file
        with open(MEDICAL_RECORDS_FILE, "w") as file:
            dump(records, file, indent=4)

        return records

# Function to save medical records to the JSON file
def save_medical_records(records):
    try:
        with open(MEDICAL_RECORDS_FILE, "w") as file:
            dump(records, file, indent=4)  # Save with indentation for readability
    except Exception as e:
        print(f"Error saving medical records: {e}")

# Function to add or update clinical notes for a patient
def add_clinical_note(email, note):
    # Get the current timestamp for the note
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format as: YYYY-MM-DD HH:MM:SS

    # Create a new note entry with the timestamp
    note_entry = {
        "note": note,
        "date_created": timestamp
    }

    # Load current medical records
    medical_records = load_or_initialize_records()

    if medical_records[email][0]["note"] == "" and medical_records[email][0]["date_created"] is None:
        medical_records[email][0] = note_entry
        with open(MEDICAL_RECORDS_FILE, "w") as file:
            dump(medical_records, file, indent=4)

    else:
        medical_records[email].append(note_entry)


    # Save the updated medical records
    save_medical_records(medical_records)

def add_patient_record():
    print("=" * 80)
    print("EDIT PATIENT RECORDS".center(80))
    print("\nEnter 'H' to return to the homepage or R to view other patient records\n")

    patient_email = input("Enter the patient's email: ").strip()
    if patient_email.upper() == "H":
        gp_page()
        return
    elif patient_email.upper() == "R":
        display_patient_records()

    registered_users = load_accounts2()
    while True:
        if patient_email not in registered_users["patient"]:
            print("\nPatient not found.\n")
            patient_email = input("Enter the patient's email: ").strip()
            if patient_email.upper() == "H":
                gp_page()
                return
        else:
            break

    note_1 = input("Enter the clinical note: ")

    add_clinical_note(patient_email, note_1)




    print("\nPatient record updated successfully.")
    sleep(2)
    gp_page()

def display_patient_records():
    print("=" * 80)
    print("ALL PATIENTS".center(80), "\n")


    # Load the JSON file
    with open('accounts.json', 'r') as file:

        database = load(file)
        ptnt_table = [{"Name": patient["name"],
                    "Surname": patient["surname"],
                    "Birthdate": patient["date_of_birth"],
                    "Email address": patient["email"]
                       }
                   for patient in database["patient"].values()
                    ]
        df_1 = pandas.DataFrame(ptnt_table)

        # Display the table using tabulate
        print(tabulate.tabulate(df_1.values, headers=df_1.columns, tablefmt="grid"))

        while True:
            ptn_email_add = input("\nEnter a patient's email address to view their record or M to return to main menu: ").strip()
            if ptn_email_add == "M":
                gp_page()
            elif ptn_email_add not in database["patient"]:
                print("\nEmail is not in the register!")
            else:
                print("\n")
                break

        patient_data = [{"Name": database["patient"][ptn_email_add]["name"],
                    "Surname": database["patient"][ptn_email_add]["surname"],
                    "Birthdate": database["patient"][ptn_email_add]["date_of_birth"],
                    "Conditions": ", ".join(database["patient"][ptn_email_add]["conditions"])
                         }
                        ]
        df_2 = pandas.DataFrame(patient_data)
        print(tabulate.tabulate(df_2.values, headers=df_2.columns, tablefmt="grid"))


        # Convert the JSON data to a list of dictionaries for the DataFrame
        medical_records = load_or_initialize_records()

        if isinstance(medical_records[ptn_email_add][0], list):
            print("Nested list detected! Fix the structure.")
            medical_records[ptn_email_add] = medical_records[ptn_email_add][0]
        data = [
            {
                "Date": item["date_created"],
                "Clinical Notes": item["note"]
            }
            for item in medical_records[ptn_email_add]
        ]

    # Create DataFrame
    df = pandas.DataFrame(data)

    # Display the table using tabulate
    print(tabulate.tabulate(df.values, headers=df.columns, tablefmt="grid"))



# Next step after seeing patient records
    while True:
        print("\n")
        print("[ 1 ] Edit patient records")
        print("[ M ] Return to main menu ")

        choice_1 = input("Please choose an option: ").strip()
        if choice_1 == "1":
            add_patient_record()
            return
        elif choice_1.upper() == "M":
            gp_page()
        else:
            print("Invalid input, please choose between: 1 or M")
# [ 4 ] Check in/out patients
# [ 5 ] Change patient details
# [ X ] Logout
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
    print("[ X ] Logout")

    while True:
        choice = input("\nPlease select and option: ").strip()
        if choice.upper() == "X":
            login_menu()
        elif choice == "1":
            print("FUNCTION NOT ADDED. WORK IN PROGRESS")   #<---------------------------Put function here.
            main_menu()
        elif choice == "2":
            print("FUNCTION NOT ADDED. WORK IN PROGRESS")   #<---------------------------Put function here.
            main_menu()
        elif choice == "3":
            mhresources(email_address=email_address)
        elif choice == "4":
            journal_page(email_address=email_address)
        elif choice == "5":
            update_account_page(email_address=email_address)
        else:
            print("Please choose a valid option '1' , '2', '3', '4', '5' or 'X'")
def gp_page():
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
        choice = input("\nPlease select and option: ").strip()
        if choice.upper() == "X":
            login_menu()
        elif choice == "1":
            print("FUNCTION NOT ADDED. WORK IN PROGRESS")   #<---------------------------Put function here.
            main_menu()
        elif choice == "2":
            print("FUNCTION NOT ADDED. WORK IN PROGRESS")   #<---------------------------Put function here.
            main_menu()
        elif choice == "3":
            display_patient_records()
        elif choice == "4":
            print("FUNCTION NOT ADDED. WORK IN PROGRESS")   #<---------------------------Put function here.
            main_menu()
        elif choice == "5":
            print("FUNCTION NOT ADDED. WORK IN PROGRESS")   #<---------------------------Put function here.
            main_menu()
        else:
            print("Please choose a valid option '1' , '2', '3', '4', '5' or 'X'")
def admins_page():
    print("=" * 80)
    print("ADMIN HOMEPAGE".center(80))
    print(termcolor.colored("Welcome, Admin. Managing the platform for better mental health!".center(80), "green"))
    print("-" * 80)
    print("[ 1 ] Add new doctor")
    print("[ 2 ] Activate/Deactivate or Delete accounts ")
    print("[ 3 ] Confirm/Un-confirm patient registration ")
    print("[ 4 ] Check in/out patients ")
    print("[ 5 ] Change patient/gp details ")
    print("[ X ] Logout")

    while True:
        choice = input("\nPlease select and option: ").strip()
        if choice.upper() == "X":
            login_menu()
        elif choice == "1":
            print("FUNCTION NOT ADDED. WORK IN PROGRESS")   #<---------------------------Put function here.
            main_menu()
        elif choice == "2":
            delete_accounts()
        elif choice == "3":
            print("FUNCTION NOT ADDED. WORK IN PROGRESS")   #<---------------------------Put function here.
            main_menu()
        elif choice == "4":
            print("FUNCTION NOT ADDED. WORK IN PROGRESS")   #<---------------------------Put function here.
            main_menu()
        elif choice == "5":
            print("FUNCTION NOT ADDED. WORK IN PROGRESS")   #<---------------------------Put function here.
            main_menu()
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
                    gp_page()
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
    try:
        ensure_pip_installed()
        install_modules()
        header()
        main_menu()
    except Exception as e:
        print(f"Excpetion is : {e}")
call_function()
#=========================================================









