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

def mhresources():
    """Function to display the main menu and navigate categories."""
    while True:
        print("\nAvailable Categories:")
        for num, category in enumerate(resources.keys(), 1):
            print(f"{num}. {category}")
        print("Type 'exit' to return to the patient homepage.")

        user_input = input("Enter the number corresponding to the category: ").strip().lower()

        if user_input == "exit":
            return "Returning to the patient homepage..."

        # Validate category selection
        try:
            category_num = int(user_input)
            if 1 <= category_num <= len(resources):
                category_name = list(resources.keys())[category_num - 1]
                return category_menu(category_name)
            else:
                print("Invalid input. Please choose a valid category number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def category_menu(category_name):
    """Function to display links for the selected category."""
    print(f"\n{category_name} Resources:")
    category_resources = resources[category_name]
    for num, (description, _) in category_resources.items():
        print(f"{num}. {description}")
    print("Type 'back' to return to the main menu.")

    while True:
        user_input = input("Enter the number corresponding to the resource: ").strip().lower()

        if user_input == "back":
            return main_menu()

        # Validate resource selection
        try:
            resource_num = int(user_input)
            if resource_num in category_resources:
                resource_description, resource_link = category_resources[resource_num]
                print(f"The link for '{resource_description}' is: {resource_link}")
                return post_selection(category_name)  # Follow-up after showing the link
            else:
                print("Invalid input. Please choose a valid resource number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def post_selection(category_name):
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
            return main_menu()
        elif user_input == "back":
            return "Returning to the patient homepage..."
        else:
            print("Invalid input. Please enter a valid option.")


# Example usage
result = mhresources()
print(result)
