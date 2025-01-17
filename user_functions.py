import json

def load_json_file(file_path):
    """Load JSON data from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": []}  # Return an empty structure if the file doesn't exist
    except json.JSONDecodeError:
        return {"users": []}  # Return an empty structure if JSON is invalid

def save_json_file(file_path, data):
    """Save data to a JSON file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def user_exists(username, file_path):
    """Check if a user exists in the JSON file."""
    data = load_json_file(file_path)
    return any(user["username"].lower() == username.lower() for user in data["users"])

def add_user(username, password, file_path):
    """Add a new user to the JSON file."""
    data = load_json_file(file_path)

    if user_exists(username, file_path):
        print("Error: User already exists.")
        return

    new_user_id = 1 if not data["users"] else data["users"][-1]["id"] + 1
    new_user = {
        "id": new_user_id,
        "username": username,
        "password": password
    }
    data["users"].append(new_user)
    save_json_file(file_path, data)
    print("User added successfully.")

def login(username, password, file_path):
    """Authenticate a user."""
    data = load_json_file(file_path)
    user = next((user for user in data["users"] if user["username"].lower() == username.lower()), None)
    return user is not None and user["password"] == password

def get_user_id(username, file_path):
    """Get the user ID from the username."""
    data = load_json_file(file_path)
    user = next((user for user in data["users"] if user["username"].lower() == username.lower()), None)
    if user:
        return user['id']
    else:
        print(f"User '{username}' not found.")
        return None

def check_history(user_id, file_path):
    """Check the game history of a user."""
    data = load_json_file(file_path)
    if not isinstance(data, list):
        print("Error: Invalid data structure.")
        return

    user_history = [game for game in data if game['user_id'] == user_id]
    if not user_history:
        print("No history found.")
        return

    print("Your History:")
    for index, game in enumerate(user_history, start=1):
        print(f"{index}. Game {index}, Category: {game['category']}, Score: {game['score']}, Date: {game['date']}")

    view_questions = input("\nDo you want to see the questions and answers? (yes/no): ").strip().lower()
    if view_questions == "yes":
        while True:
            try:
                game_choice = int(input("Which game? (Enter the game number): ").strip())
                if 1 <= game_choice <= len(user_history):
                    selected_game = user_history[game_choice - 1]
                    print(f"\nQuestions and Answers for Game {game_choice}:")
                    for q in selected_game["questions"]:
                        print(f" - Question: {q['question']}")
                        print(f"   Your Answer: {q['user_answer']}")
                        print(f"   Correct: {'Yes' if q['is_correct'] else 'No'}")
                    break
                else:
                    print("Invalid game number.")
            except ValueError:
                print("Invalid input. Please enter a valid game number.")