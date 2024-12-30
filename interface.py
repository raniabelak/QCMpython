import json
import user_functions as uf
import admin_functions as af
import quiz_app as quiz

def admin_menu():
    """Admin menu for managing categories and questions."""
    while True:
        print("\nAdmin Menu:")
        print("1. Add a new category or question")
        print("2. Delete a category")
        print("3. Delete a question")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            af.add_category_or_question('questions.json')
        elif choice == "2":
            af.delete_category('questions.json')
        elif choice == "3":
            af.delete_question('questions.json')
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

def user_menu(user_name):
    """User menu for managing history or starting a new game."""
    while True:
        print("\nUser Menu:")
        print("1. Check your history")
        print("2. Start a new game")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            user_id = uf.get_user_id(user_name)
            uf.check_history(user_id, 'history.json')
        elif choice == "2":
            quiz.start_quiz(user_name)
        elif choice == "3":
            print("See you next time!")
            break
        else:
            print("Invalid choice. Please try again.")

def login_or_signup():
    """Handle login or signup process."""
    user_name = input("Enter your username: ").strip()

    if uf.user_exists(user_name, 'users.json'):
        # User exists, ask for password
        for _ in range(3):  # Allow 3 attempts to enter the password
            password = input("Enter your password: ").strip()
            if uf.login(user_name, password, 'users.json'):
                print(f"Welcome {user_name}!! You have been logged in successfully.")
                user_menu(user_name)  # Redirect to user menu
                return
            else:
                print("Invalid password. Please try again.")
        print("Too many failed attempts. Please try again later.")
    else:
        # User doesn't exist, sign up
        print(f"Welcome {user_name}! It seems you are new here. Let's sign you up.")
        password = input("Enter a password to create your account: ").strip()
        uf.add_user(user_name, password, 'users.json')
        print(f"Your account has been created successfully, {user_name}!")
        login_or_signup()  # Loop back to login after signup


def main():
    print("WELCOME TO THE QUIZ GAME !!")
    is_admin = input("Are you an admin? (yes/no): ").strip().lower()

    if is_admin == "yes":
        admin_code = input("Enter the admin code: ").strip()
        if admin_code == "Admin2025":
            print("Welcome Admin!")
            admin_menu()
        else:
            print("Invalid code. Please try again.")
    else:
        login_or_signup()

if __name__ == "__main__":
    main()         