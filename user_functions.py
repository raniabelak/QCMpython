import json

# fonction pour vérifier si un utilisateur existe
def user_exists(user_name, file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        exit("File not found.")
    
    user = next((usr for usr in data["users"] if usr["username"].lower() == user_name.lower()), None)
    return user is not None

# fonction pour ajouter un utilisateur
def add_user(user_name, password, file_path):
    try:
        with open(file_path,'r',encoding='UTF-8') as file:
            data = json.load(file)
    except:
        data = {"users": []}

    new_user_id = 1 if not data["users"] else data["users"][-1]["id"] + 1
    
    user = {
        "id": new_user_id,
        "username": user_name,
        "password": password
    }
    data["users"].append(user)

    with open(file_path, 'w', encoding='UTF-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    print("User added successfully.")

    
# fonction pour se connecter
def login(user_name, password, file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)  
    except FileNotFoundError:
        exit("File not found.")

    user = next((usr for usr in data["users"] if usr["username"].lower() == user_name.lower()), None)
    if user:
        return user["password"] == password
    else:
        return False

# Function to get user ID from username
def get_user_id(username):
    try:
        with open('users.json', 'r', encoding='utf-8') as file:
            users_data = json.load(file)
    except FileNotFoundError:
        print("No user data available.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON from 'users.json'.")
        return None

    user = next((u for u in users_data.get("users", []) if u['username'].lower() == username.lower()), None)
    if user:
        return user['id']
    else:
        print(f"User '{username}' not found.")
        return None

# Function to check the history of a user
def check_history(user_id, file_path):
    # Load the data directly from the file
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
        print("Your History :")
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
        print(f"No history found.")