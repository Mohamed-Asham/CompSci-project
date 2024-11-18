# Delete Information

class User:
    def __init__(self, name, user_type):
        self.name = name
        self.user_type = user_type


users = [
    User("John", "MHWP"),
    User("Alice", "Patient")
]


def delete_user(users, user_name, password):
    for user in users:
        if user.name == user_name:
            for attempt in range(3):
                pass_word = input('Confirm your password: ')
                if pass_word == password:
                    users.remove(user)
                    print(f"User {user_name} has been deleted.")
                    break
                else:
                    if attempt < 2:
                        print(f"Password is incorrect. You have {2 - attempt} attempts left.")
                    else:
                        print("Password incorrect. You have run out of attempts. Please reset password.")
            break
    else:
        print('Incorrect username. Please enter the correct username. ')
