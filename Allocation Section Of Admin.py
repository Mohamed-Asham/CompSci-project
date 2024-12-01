from tabulate import tabulate

def allocation_management_system():
    # User class definition
    class User:
        def __init__(self, name, user_type):
            self.name = name
            self.user_type = user_type
            self.is_disabled = False  # Set the initial disabled status to False

    # Initial data setup
    patients_ = []
    MHWPs_ = []

    users = [
        User('Alice Smith', 'Patient'), User('Jane Ellie', 'Patient'),
        User('Mackle Moore', 'Patient'), User('Onika Tanya', 'Patient'),
        User('Benny Daniels', 'Patient'), User('Danny Phantom', 'Patient'),
        User('Steven Carr', 'Patient'), User('John Mike', 'MHWP'),
        User('Julie Mitchell', 'MHWP'), User('Adam Scott', 'MHWP')
    ]

    for user in users:
        if user.user_type.lower() == 'patient':
            patient_info = {'name': user.name.lower(), 'user_type': user.user_type.lower()}
            patients_.append(patient_info)
        elif user.user_type.lower() == 'mhwp':
            MHWP_info = {'name': user.name.lower(), 'user_type': user.user_type.lower()}
            MHWPs_.append(MHWP_info)

    # Dictionary to store allocations
    allocations = {mhwp['name']: [] for mhwp in MHWPs_}  # Each MHWP has a list of assigned patients

    # Automated allocation
    def automated_allocation():
        print("\nAutomating patient allocations...\n")
        unallocated_patients = [p for p in patients_ if not any(p["name"] in patients for patients in allocations.values())]

        for patient in unallocated_patients:
            # Find the MHWP with the least number of patients
            mhwp_w_least_patients = min(allocations, key=lambda mhwp: len(allocations[mhwp]))
            allocations[mhwp_w_least_patients].append(patient["name"])

        print("All patients have been automatically assigned to MHWPs.\n")

    # Display allocations in a tabular format
    def display_allocations():
        print("\nCurrent Allocations:")
        table_data = []

        # Prepare data for the table
        for mhwp, patients in allocations.items():
            if patients:
                patients_list = ', '.join([p.title() for p in patients])
            else:
                patients_list = "No patients assigned"
            table_data.append([mhwp.title(), patients_list])

        # Define table headers
        headers = ["MHWP", "Assigned Patients"]

        # Print the table using tabulate
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    # Manual handling of allocations
    def manual_allocation():
        print("\nCurrent Allocations:")
        display_allocations()

        # Select Patient to Reassign
        patient_name = input("\nEnter the name of the patient to reassign (or type 'exit' to cancel): ").lower()
        if patient_name == 'exit':
            return

        selected_patient = next((p for p in patients_ if p["name"] == patient_name), None)
        if not selected_patient:
            print("Invalid patient name. Please try again.")
            return

        # Check if the patient is already assigned to an MHWP
        current_mhwp = next((mhwp for mhwp, patients in allocations.items() if patient_name in patients), None)

        if current_mhwp:
            print(f"Patient {patient_name.title()} is currently assigned to {current_mhwp.title()}.")
            reassignment = input("Would you like to reassign this patient? (yes/no): ").lower()
            if reassignment != 'yes':
                print("Reallocation cancelled!")
                return
            # Remove Patient from Current MHWP
            allocations[current_mhwp].remove(patient_name)
            print(f"Patient {patient_name.title()} has been removed from {current_mhwp.title()}.")
        else:
            print(f"Patient {patient_name.title()} is unassigned.")

        # Select New MHWP
        print("\nAvailable MHWPs:")
        for idx, mhwp in enumerate(MHWPs_):
            print(f"{idx + 1}. {mhwp['name'].title()}")
        mhwp_name = input("Enter the name of the MHWP to assign the patient to: ").lower()

        selected_mhwp = next((m for m in MHWPs_ if m["name"] == mhwp_name), None)
        if not selected_mhwp:
            print("Invalid MHWP name. Please try again.")
            return

        # Add Patient to New MHWP
        allocations.setdefault(mhwp_name, []).append(patient_name)
        print(f"Patient {patient_name.title()} has been reassigned to MHWP {mhwp_name.title()}.")

    # Allocation menu
    def allocation_menu():
        automated_allocation()

        while True:
            print("\nSelect an action:")
            print("[1] View Current Allocations")
            print("[2] Reassign a Patient (Manual Adjustment)")
            print("[X] Exit")

            choice = input("Please select an option: ")

            if choice == '1':
                display_allocations()
            elif choice == '2':
                manual_allocation()
            elif choice.lower() == 'x':
                print("Exiting allocation management.")
                break
            else:
                print("Invalid choice. Please try again.")

    # Run the allocation menu
    allocation_menu()

# Call the function
allocation_management_system()
