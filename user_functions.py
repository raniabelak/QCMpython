import json
import os
import sys

def get_base_path():
    """
    Dynamically resolves the base path for file operations.
    - If running as an executable, returns the temporary directory created by PyInstaller.
    - If running as a script, returns the directory of the script.
    """
    if getattr(sys, 'frozen', False):  # Check if the script is running as an executable
        return sys._MEIPASS  # Use the temporary directory created by PyInstaller
    else:
        return os.path.dirname(os.path.abspath(__file__))  # Use the script's directory

def get_file_path(filename):
    """
    Resolves the full path for a file based on the base path.
    """
    return os.path.join(get_base_path(), filename)

def user_exists(user_name, file_name):
    """
    Checks if a user exists in the users file.
    """
    file_path = get_file_path(file_name)  # Resolve the file path
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Error: The users file is missing.")
        return False
    except json.JSONDecodeError:
        print("Error: The users file contains invalid JSON.")
        return False

    user = next((usr for usr in data["users"] if usr["username"].lower() == user_name.lower()), None)
    return user is not None

def add_user(user_name, password, file_name):
    """
    Adds a new user to the users file.
    """
    file_path = get_file_path(file_name)  # Resolve the file path
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"users": []}
    except json.JSONDecodeError:
        print("Error: The users file contains invalid JSON.")
        return

    new_user_id = 1 if not data["users"] else data["users"][-1]["id"] + 1
    
    user = {
        "id": new_user_id,
        "username": user_name,
        "password": password
    }
    data["users"].append(user)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    print("User added successfully.")

def login(user_name, password, file_name):
    """
    Authenticates a user by checking their username and password.
    """
    file_path = get_file_path(file_name)  # Resolve the file path
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Error: The users file is missing.")
        return False
    except json.JSONDecodeError:
        print("Error: The users file contains invalid JSON.")
        return False

    user = next((usr for usr in data["users"] if usr["username"].lower() == user_name.lower()), None)
    if user:
        return user["password"] == password
    else:
        return False

def get_user_id(username, file_name):
    """
    Retrieves the user ID for a given username.
    """
    file_path = get_file_path(file_name)  # Resolve the file path
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            users_data = json.load(file)
    except FileNotFoundError:
        print("Error: The users file is missing.")
        return None
    except json.JSONDecodeError:
        print("Error: The users file contains invalid JSON.")
        return None

    user = next((u for u in users_data.get("users", []) if u['username'].lower() == username.lower()), None)
    if user:
        return user['id']
    else:
        print(f"User '{username}' not found.")
        return None

def check_history(user_id, file_name):
    """
    Displays the quiz history for a specific user.
    """
    file_path = get_file_path(file_name)  # Resolve the file path
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Error: The history file is missing.")
        return
    except json.JSONDecodeError:
        print("Error: The history file contains invalid JSON.")
        return

    # Ensure data is in the correct structure
    if not isinstance(data, list):
        print("Error: Invalid data structure. Expected a list of games.")
        return

    # Filter the history based on user_id
    user_history = [game for game in data if game['user_id'] == user_id]

    if user_history:
        print("Your History:")
        for index, game in enumerate(user_history, start=1):
            print(f"{index}. Game {index}, Category: {game['category']}, Score: {game['score']}, Date: {game['date']}")

        # Ask if the user wants to see the questions and answers
        view_questions = input("\nDo you want to see the questions and answers? (yes/no): ").strip().lower()
        if view_questions == "yes":
            # Ask which game the user wants to view
            try:
                game_choice = int(input("Which game? (Enter the game number): ").strip())
                if 1 <= game_choice <= len(user_history):
                    selected_game = user_history[game_choice - 1]
                    print(f"\nQuestions and Answers for Game {game_choice}:")
                    for q in selected_game["questions"]:
                        print(f" - Question: {q['question']}")
                        print(f"   Your Answer: {q['user_answer']}")
                        print(f"   Correct: {'Yes' if q['is_correct'] else 'No'}")
                else:
                    print("Invalid game number.")
            except ValueError:
                print("Invalid input. Please enter a valid game number.")
    else:
        print("No history found.")

# Example usage
if __name__ == "__main__":
    users_file = "users.json"  # Replace with your users file name
    history_file = "history.json"  # Replace with your history file name

    # Example: Add a new user
    add_user("test_user", "password123", users_file)

    # Example: Check if a user exists
    if user_exists("test_user", users_file):
        print("User exists!")

    # Example: Login
    if login("test_user", "password123", users_file):
        print("Login successful!")
    else:
        print("Login failed.")

    # Example: Get user ID
    user_id = get_user_id("test_user", users_file)
    if user_id:
        print(f"User ID: {user_id}")

    # Example: Check user history
    check_history(user_id, history_file)