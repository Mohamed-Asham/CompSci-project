 #======================MHWP Functions======================
def add_patient_record():
    print("=" * 80)
    print("MANAGE PATIENT RECORDS".center(80))
    print("\nEnter 'H' to return to the homepage\n")

    patient_email = input("Enter the patient's email: ").strip()
    if patient_email.upper() == "H":
        gp_page()
        return

    while True:
        if patient_email not in registered_users["patient"]:
            print("\nPatient not found.\n")
            patient_email = input("Enter the patient's email: ").strip()
            if patient_email.upper() == "H":
                gp_page()
                return
        else:
            break

    patient = registered_users["patient"][patient_email]

    # Adding predefined mental conditions
    conditions = ["Anxiety", "Depression", "Autism", "PTSD", "Bipolar Disorder"]
    print("\nAvailable Mental Conditions:")
    for i, condition in enumerate(conditions, 1):
        print(f"[ {i} ] {condition}")
    print("[ 0 ] Add custom condition")

    selected_conditions = []
    while True:
        choice = input("Select a condition by number (or press Enter to finish): ").strip()
        if choice == "":
            break
        elif choice == "0":
            custom_condition = input("Enter a custom condition: ").strip()
            if custom_condition:
                selected_conditions.append(custom_condition)
        elif choice.isdigit() and 1 <= int(choice) <= len(conditions):
            selected_conditions.append(conditions[int(choice) - 1])
        else:
            print("Invalid choice. Try again.")

    # Adding notes
    notes = input("Enter notes about the patient: ").strip()

    # Saving record
    if "records" not in patient:
        patient["records"] = []
    patient["records"].append({"conditions": selected_conditions, "notes": notes})
    save_accounts(registered_users)

    print("\nPatient record updated successfully.")
    sleep(2)
    gp_page()

def display_patient_dashboard():
    print("=" * 80)
    print("PATIENT DASHBOARD".center(80))
    print("\nEnter 'H' to return to the homepage\n")

    for patient_email, patient_data in registered_users["patient"].items():
        print(f"\nPatient: {patient_data['name']} {patient_data['surname']} ({patient_email})")
        print("-" * 80)
        if "records" in patient_data:
            for record in patient_data["records"]:
                print(f"Conditions: {', '.join(record['conditions'])}")
                print(f"Notes: {record['notes']}")
        else:
            print("No records available.")

        if "mood_tracking" in patient_data:
            print("\nMood Tracking Chart:")
            plot_mood_chart(patient_data["mood_tracking"])

    input("\nPress Enter to return to the homepage.")
    gp_page()

def plot_mood_chart(mood_tracking):
    import matplotlib.pyplot as plt
    dates = [entry["date"] for entry in mood_tracking]
    moods = [entry["mood"] for entry in mood_tracking]

    plt.plot(dates, moods, marker="o")
    plt.title("Mood Tracking Over Time")
    plt.xlabel("Date")
    plt.ylabel("Mood")
    plt.grid()
    plt.show()

# Add these options to the GP Homepage menu:
def gp_page():
    print("=" * 80)
    print("GP HOMEPAGE".center(80))
    print(termcolor.colored("Welcome, GP. Your dedication helps patients achieve their best mental health.".center(80), "green"))
    print("[ 1 ] View schedule")
    print("[ 2 ] Manage appointments ")
    print("[ 3 ] Manage patient records")
    print("[ 4 ] Add patient record ")
    print("[ 5 ] View patient dashboard ")
    print("[ X ] Logout")

    while True:
        choice = input("\nPlease select an option: ").strip()
        if choice.upper() == "X":
            login_menu()
        elif choice == "1":
            print("FUNCTION NOT ADDED. WORK IN PROGRESS")
            main_menu()
        elif choice == "2":
            print("FUNCTION NOT ADDED. WORK IN PROGRESS")
            main_menu()
        elif choice == "3":
            print("FUNCTION NOT ADDED. WORK IN PROGRESS")
            main_menu()
        elif choice == "4":
            add_patient_record()
        elif choice == "5":
            display_patient_dashboard()
        else:
            print("Please choose a valid option.")## 