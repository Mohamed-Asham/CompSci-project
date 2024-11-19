
def update_account_page(email_address):
    data=load_accounts()
    account_details= data["patient"][email_address]
    print("These are your current account details:\n")
    counter=1
    for key,value in account_details.items():
        if key != "password":
            print("[",counter,"] ",(key[0].upper())+key[1:len(key)].replace("_"," "),": ",value)
            counter+=1
    print("\n")
    update_option = int(input("Please select a option to edit:"))

    if update_option == 1:
        while True:
            new_email= input("Please enter your new email address:").strip()
            email_pattern = r"^[\w\.-]+@[\w\.-]+\.[\w\.-]+$"
            email_check = checking_email(new_email)

            if email_check == "Email already registered":
                print("This email is already registered. Please use a different email.")
            else:
                if match(email_pattern, new_email):
                    break
                elif not match(email_pattern, new_email):
                    print("Invalid email format. Please enter a valid email.")
                else:
                    print("Invalid email format. Please enter a valid email.")
        account_details["email"]= new_email
        del data["patient"][email_address]
        data["patient"][new_email]= account_details
        with open("accounts.json", "w") as file:
            json.dump(data, file ,indent=4)
        print("Your email has been updated successfully.")
        patients_page(new_email)

    elif update_option ==2:
        new_first_name = input("Please enter your new first name: ").strip()
        account_details["name"]= new_first_name
        data["patient"][email_address]= account_details
        with open("accounts.json", "w") as file:
            json.dump(data, file, indent=4)
        print("Your name has been upodated successfully")
        patients_page(email_address)

    elif update_option == 3:
        new_surname = input("Please enter your new surname").strip()
        account_details["surname"]= new_surname
        data["patient"][email_address]= account_details
        with open("accounts.json", "w") as file:
            json.dump(data, file, indent=4)
        print("Your surname has been upodated successfully")
        patients_page(email_address)

    elif update_option == 4:
        while True:
            new_birthday = input("Birth date (DD/MM/YYYY): ").strip()  # Pad single digit day with zero if necessary
            try:
                new_birthday.zfill(2)
                day, month, year = new_birthday.split("/")
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
                    datetime.strptime(new_birthday, "%d/%m/%Y")
                    break
            except Exception:
                print(f"Invalid birth date, try again.")
        account_details["date_of_birth"] = new_birthday
        data["patient"][email_address] = account_details
        with open("accounts.json", "w") as file:
            json.dump(data, file, indent=4)
        print("Your date of birth has been upodated successfully")
        patients_page(email_address)


    elif update_option == 5:
        while True:
            print("Genders:")
            print("[ 1 ] Male")
            print("[ 2 ] Female")
            try:
                new_gender = input("Please choose an option: ").strip()
                if new_gender == "1":
                    new_gender = "Male"
                    break
                elif new_gender == "2":
                    new_gender = "Female"
                    break
                else:
                    print("Please choose a valid option '1' or '2'")
            except Exception:
                print("Invalid option")
        account_details["gender"] = new_gender
        data["patient"][email_address] = account_details
        with open("accounts.json", "w") as file:
            json.dump(data, file, indent=4)
        print("Your gender has been upodated successfully")
        patients_page(email_address)

    elif update_option == 6:
        while True:
            print("NHS blood donor:")
            print("[ 1 ] Yes")
            print("[ 2 } No")
            try:
                a_new = input("Please choose an option: ").strip()
                if a_new == "1":
                    a_new = "IS Blood donor"
                    break
                elif a_new == "2":
                    a_new = "NOT Blood donor"
                    break
                else:
                    print("Please choose '1', '2'")
            except Exception:
                print("Invalid option")
        account_details["NHS_blood_donor"] = a_new
        data["patient"][email_address] = account_details
        with open("accounts.json", "w") as file:
            json.dump(data, file, indent=4)
        print("Your NHS blood donor status has been upodated successfully")
        patients_page(email_address)

    elif update_option == 7:

        while True:
            print("NHS organ donor:")
            print("[ 1 ] Yes")
            print("[ 2 } No")

            try:
                b_new = input("Please choose an option: ").strip()
                if b_new == "1":
                    b_new = "IS Organ donor"
                    break
                elif b_new == "2":
                    b_new = "NOT Organ donor"
                    break
                else:
                    print("Please choose '1', '2' or 'M' to return to menu")
            except Exception:
                print("Invalid option")
        account_details["NHS_organ_donor"] = b_new
        data["patient"][email_address] = account_details
        with open("accounts.json", "w") as file:
            json.dump(data, file, indent=4)
        print("Your NHS organ donor status has been upodated successfully")
        patients_page(email_address)

    elif update_option == 8:
        while True:
            try:
                ad1_new = input("Address Line 1 (House number, street name): ")
                address_line_1_pattern = r"^\d+\s+[\w\s\-']+(\s+(Apt|Suite|St|Rd|Lane|Blvd|Ave|Dr|Court|Pl|Road|Street|Way|Close))?(\s*\d*[A-Za-z]?)?$"
                if match(address_line_1_pattern, ad1_new):
                    break
                else:
                    print("Address Line 1 is not valid.")
            except Exception:
                print("Invalid address, try again")
        account_details["Address_Line_1"] = ad1_new
        data["patient"][email_address] = account_details
        with open("accounts.json", "w") as file:
            json.dump(data, file, indent=4)
        print("Your Address Line 1 has been upodated successfully")
        patients_page(email_address)

    elif update_option == 9:
        while True:
            try:
                ad2_new = input("Address Line 2 (Postcode, zipcode, or country): ")
                address_line_2_pattern = r'^[A-Za-z0-9\s,]+$'
                if match(address_line_2_pattern, ad2_new):
                    break
                else:
                    print("Address Line 1 is not valid.")
            except Exception:
                print("Invalid address, try again")
        account_details["Address_Line_2"] = ad2_new
        data["patient"][email_address] = account_details
        with open("accounts.json", "w") as file:
            json.dump(data, file, indent=4)
        print("Your Address Line 2 has been upodated successfully")
        patients_page(email_address)



















