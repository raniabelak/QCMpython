import user_functions as uf
import admin_functions as af
import quiz_app as quiz_app

def admin_menu():
    """Admin menu for managing categories and questions."""
    while True:
        print("\nMenu:")
        print("1. Add a category")
        print("2. Add a question")
        print("3. Delete a category")
        print("4. Delete a question")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            af.add_category('qcm.json')
        elif choice == "2" :
            af.add_question('qcm.json')
        elif choice == "3":
            af.delete_category('qcm.json')
        elif choice == "4":
            af.delete_question('qcm.json')
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def user_menu(username):
    """User menu for managing history or starting a new game."""
    while True:
        print("\nUser Menu:")
        print("1. Check your history")
        print("2. Start a new game")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            user_id = uf.get_user_id(username, 'users.json')
            if user_id:
                uf.check_history(user_id, 'history.json')
        elif choice == "2":
            quiz_app.start_quiz(username)
        elif choice == "3":
            print("See you next time!")
            break
        else:
            print("Invalid choice. Please try again.")

def login_or_signup():
    """Handle login or signup process."""
    while True:
        username = input("Enter your username: ").strip()
        if username:
            break
        print("Error: Username cannot be empty.")

    if uf.user_exists(username, 'users.json'):
        # User exists, ask for password
        while True:
            password = input("Enter your password: ").strip()
            if uf.login(username, password, 'users.json'):
                print(f"Welcome {username}!! You have been logged in successfully.")
                user_menu(username)  # Redirect to user menu
                return
            else:
                print("Invalid password. Please try again.")
        
    else:
        # User doesn't exist, sign up
        print(f"Welcome {username}! It seems you are new here. Let's sign you up.")
        while True:
            password = input("Enter a password to create your account: ").strip()
            if password:
                break
            print("Error: Password cannot be empty.")

        uf.add_user(username, password, 'users.json')
        print(f"Your account has been created successfully, {username}!")
        login_or_signup()  # Loop back to login after signup

def main():
    print("WELCOME TO THE QUIZ GAME !!")
    while True:
       is_admin = input("Are you an admin? (yes/no): ").strip().lower()
       if is_admin in ["yes", "no"]:
            break

    if is_admin == "yes":
        while True:
            admin_code = input("Enter the admin code: ").strip()
            if admin_code == "Admin2025":
                print("Welcome Admin!")
                admin_menu()
                break
            else:
                print("Invalid code. Please try again.")
    else:
        login_or_signup()

if __name__ == "__main__":
    main()