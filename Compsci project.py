
#=======================Modules=============================
from importlib import import_module
from time import sleep
from sys import exit, executable
from re import match
from random import randint
from datetime import datetime
from json import load, dump
from platform import system
from os import path
import subprocess
# List of required non-standard packages
required_packages = ["pyfiglet", "termcolor"]
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
            return data
    except FileNotFoundError:
        # Return default accounts if the file doesn't exist
        return {
            "patient": {"patient1@gmail.com": "password1"},
            "gp": {"gp1@gmail.com": "password1"},
            "admin": {"admin1@gmail.com": "password1"}
        }
    except Exception:
        return {
            "patient": {"patient1@gmail.com": "password1"},
            "gp": {"gp1@gmail.com": "password1"},
            "admin": {"admin1@gmail.com": "password1"}
        }
def save_accounts(new_account=None):
    with open(DATA_FILE, "w") as file:
        dump(new_account, file, indent=4)
registered_users = load_accounts()
#==========================================================


#======================Admin Homepage======================
def display_all_accounts():
    print("=" * 45)
    print("ALL ACCOUNTS".center(45))
    print("\nEnter 'H' to return to the homepage")

    if not registered_users:
        print("No accounts available.")
        return

    account_mapping = {}
    counter = 1

    for role, accounts in registered_users.items():
        print(f"\nRole: {role.capitalize()}")
        print("-" * 45)
        if accounts:
            for email, password in accounts.items():
                print(f"[ {counter} ] Email: {email}, Password: {password}")
                account_mapping[counter] = (role, email)  # Map the number to role and email
                counter += 1
        else:
            print("No accounts in this role.")
    print(f"\n{"=" * 45}")

    return account_mapping
def delete_accounts():
    account_mapping = display_all_accounts()
    print("\nEnter 'H' to return to the homepage\n")

    while True:
        choice = input("Enter the numeber of the account to delete: ").strip()
        if choice.upper() == "H":
            admins_page()
            return

        if not choice.isdigit():
            print("Invalid input. Please enter a number corresponding to an account.")
            continue

        account_number = int(choice)
        if account_number not in account_mapping:
            print(f"Invalid selection. No account corresponds to number {account_number}.")
            continue

        role, email_to_delete = account_mapping[account_number]
        confirming_option = input(f"Confirm deletion of account [ {account_number} ] [ {email_to_delete} ] (Y/N): ").strip().upper()
        if confirming_option == "Y":
            del registered_users[role][email_to_delete]
            save_accounts(registered_users)
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
#...
#==========================================================


#=======================GP Homepage========================
#....
#==========================================================


#====================Homepage Accounts=====================
def patients_page():
    print("=" * 45)
    print("PATIENT HOMEPAGE".center(45))
    print(termcolor.colored("Welcome, Patient. Ready to take the next step in your well-being journey?".center(45), "green"))
    print("-" * 45)
    print("[ 1 ] Book and manage appointments")
    print("[ 2 ] Change default GP ")
    print("[ 3 ] Change account details")
    print("[ X ] Logout")

    while True:
        choice = input("\nPlease select and option: ")
        if choice.upper() == "X":
            login_menu()
        elif choice == "1":
            print("FUNCTION NOT ADDED. WORK IN PROGRESS")   #<---------------------------Put function here.
            main_menu()
        elif choice == "2":
            print("FUNCTION NOT ADDED. WORK IN PROGRESS")   #<---------------------------Put function here.
            main_menu()
        elif choice == "3":
            print("FUNCTION NOT ADDED. WORK IN PROGRESS")   #<---------------------------Put function here.
            main_menu()
        else:
            print("Please choose a valid option '1' , '2', '3', or 'X'")
def gp_page():
    print("=" * 45)
    print("GP HOMEPAGE".center(45))
    print(termcolor.colored("Welcome, GP. Your dedication helps patients achieve their best mental health.".center(45), "green"))
    print("[ 1 ] View schedule")
    print("[ 2 ] Manage appointments ")
    print("[ 3 ] Manage patient records")
    print("[ 4 ] Check in/out patients ")
    print("[ 5 ] Change patient details ")
    print("[ X ] Logout")

    while True:
        choice = input("\nPlease select and option: ")
        if choice.upper() == "X":
            login_menu()
        elif choice == "1":
            print("FUNCTION NOT ADDED. WORK IN PROGRESS")   #<---------------------------Put function here.
            main_menu()
        elif choice == "2":
            print("FUNCTION NOT ADDED. WORK IN PROGRESS")   #<---------------------------Put function here.
            main_menu()
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
def admins_page():
    print("=" * 45)
    print("ADMIN HOMEPAGE".center(45))
    print(termcolor.colored("Welcome, Admin. Managing the platform for better mental health!".center(45), "green"))
    print("-" * 45)
    print("[ 1 ] Add new doctor")
    print("[ 2 ] Activate/Deactivate or Delete accounts ")
    print("[ 3 ] Confirm/Un-confirm patient registration ")
    print("[ 4 ] Check in/out patients ")
    print("[ 5 ] Change patient details ")
    print("[ X ] Logout")

    while True:
        choice = input("\nPlease select and option: ")
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
    if role not in registered_users:
        return "Invalid role"
    role_accounts = registered_users[role]
    if email in role_accounts:
        if role_accounts[email] == v_password:
            return True
        else:
            return "Incorrect password"
    else:
        return "Email not found"
def checking_email(email):
    for role_accounts in registered_users.values():
        if email in role_accounts:
            return "Email already registered"
    return "Email available"
def registering_user():
    print("=" * 45)
    print("REGISTERING".center(45))
    print("Please enter your details \n\nEnter 'M' to return to main menu\n")
    first_name = input("First name: ")
    if first_name.upper() == "M":
        main_menu()
    sur_name = input("Last name: ")
    if sur_name.upper() == "M":
        main_menu()

    while True:
        date_input = input("Birth date (DD/MM/YYYY): ")  # Pad single digit day with zero if necessary
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
        role = input("Are you a Patient or GP? : ")
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
        email_address = input("Email address: ")
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
        input_password = input("Password [8 characters min, 1 uppercase letter min, and 1 number min]: ")
        if input_password.upper() == "M":
            main_menu()

        has_upper = False
        has_digit = False
        password_pattern = r'^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'

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
            user_gender = input("Please choose an option: ")
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

    while True:
        print ("NHS blood donor:")
        print ("[ 1 ] Yes")
        print ("[ 2 } No")

        try:
            a = input("Please choose an option: ")
            if a.upper() == "M":
                main_menu()

            if a == "1":
                a = "Is a blood donor"
                break
            elif a=="2":
                a = "Is NOT a blood donor"
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
            b = input("Please choose an option: ")
            if b.upper() == "M":
                main_menu()

            if b == "1":
                b = "Is an organ donor"
                break
            elif b=="2":
                b = "Is NOT an organ donor"
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
            address_line_1_pattern = r"^\d+\s+[A-Za-z]+(\s+[A-Za-z]+)*(\s+(Apt|Suite|St|Rd|Lane|Blvd|Ave|Dr|Court|Pl))?(\s*\d+[A-Za-z]?)?$"

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

    user = Accounts(email_address, input_password, first_name, sur_name,
                               date_input, user_gender, role, a, b, ad1, ad2)

    print("Your account has been made.")
    print("Current account is being registered to system...")
    sleep(3)
    print("Returing to main menu.")
    sleep(1)
class Accounts:
    dictionary_of_accounts = {}
    def __init__(self, email, a_password, name, surname, date_of_birth, gender,
                 job_role, nhs_blood_donor, nhs_organ_donor, address_line_1, address_line_2 ):
        self.email = email
        self.password = a_password
        self.name = name
        self.surname = surname
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.job_role = job_role
        self.NHS_blood_donor = nhs_blood_donor
        self.NHS_organ_donor = nhs_organ_donor
        self.Address_Line_1 = address_line_1
        self.Address_Line_2 = address_line_2

        Accounts.dictionary_of_accounts[email] = self
        self.add_to_role_accounts()


    def __repr__(self):
        return (f"Accounts(email='{self.email}', name='{self.name}', surname='{self.surname}', "
                f"date_of_birth='{self.date_of_birth}', gender='{self.gender}', job_role='{self.job_role}', "
                f"NHS_blood_donor='{self.NHS_blood_donor}', NHS_organ_donor='{self.NHS_organ_donor}', "
                f"Address_Line_1='{self.Address_Line_1}', Address_Line_2='{self.Address_Line_2}')")

    def add_to_role_accounts(self):
        # Add the account directly to the appropriate role in registered_users
        if self.job_role in registered_users:
            registered_users[self.job_role][self.email] = self.password
        else:
            # If the role does not exist, create it (though this shouldn't normally happen)
            registered_users[self.job_role] = {self.email: self.password}

        # Save the updated registered_users dictionary to the JSON file
        save_accounts(registered_users)

    @classmethod
    def display_all_accounts(cls):
        if cls.dictionary_of_accounts:
            print("All registered accounts:")
            for email, account in cls.dictionary_of_accounts.items():
                print(f"Email: {email}, Account Details: {account}")
        else:
            print("No accounts have been registered yet.")
#==========================================================


#==================Login Function==========================
def reset_password():
    print("=" * 45)
    print("PASSWORD RESET".center(45))
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

        if new_password == registered_users[roless][email_addresss]:
            print("New password cannot be same as previous password")
            tries -= 1
        elif not match(password_pattern, new_password):
            print("Password is weak, try a stronger password")
            tries -= 1
        elif tries == 1:
            print("Too many incorrect inputs. Returning to main menu")
        else:
            confirm_password = input("Confirm password: ")
            if confirm_password != new_password:
                print("Passwords do not match, please enter password again")
            else:
                break

    registered_users[roless][email_addresss] = new_password
    save_accounts(registered_users)
    print("Password reset successfully.")
    main_menu()
    return
def login_user(role):
    print("-" * 45)
    print("Please enter your details \n\nEnter 'R' to return to reset password\nEnter 'M' to return to main menu\n")

    login_attempts = 10
    while login_attempts > 0:
        email_address = input("Email address: ")
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

            if email_address in registered_users["admin"] and registered_users["admin"][email_address] == login_password:
                print("Admin login successful")
                admins_page()

            result = verify_credentials(email_address, login_password, role=role)

            if result == True:
                print(f"{role.capitalize()} login successful")
                if role == "patient":
                    patients_page()
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
        print("=" * 45)
        print("LOGIN AS:".center(45))
        print("[ 1 ] Patient")
        print("[ 2 ] GP")
        print("[ 3 ] Admin")
        print("[ M ] Main menu")
        print("[ E ] Exit")

        user = input("Please choose an option: ")
        if user == "1":
            login_user("patient")
        elif user == "2":
            login_user("gp")
        elif user == "3":
            login_user("admin")
        elif user.upper() == "E":
            print("=" * 45)
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
        print("=" * 45)
        print("UCL Management System".center(45))
        print("[ 1 ] Login")
        print("[ 2 ] Register")
        print("[ E ] Exit")

        choice = input("Please choose an option: ")
        if choice == "1":
            login_menu()
        elif choice == "2":
            registering_user()
        elif choice.upper() == "E":
            print("=" * 45)
            print("EXITING!".center(45))
            # uninstall_modules()
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









