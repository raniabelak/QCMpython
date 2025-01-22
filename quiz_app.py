import json
import random
import datetime
import time
import user_functions as uf
import os
import sys

# Dynamically resolves the base path for file operations
def get_base_path():
    if getattr(sys, 'frozen', False):  # Check if the script is running as an executable
        return sys._MEIPASS  # use pyinstaller temp directory
    else:
        return os.path.dirname(os.path.abspath(__file__))  # use script directory

# Resolves the full path for a file based on the base path
def get_file_path(filename):
    return os.path.join(get_base_path(), filename)
def load_json_file(filename):
    file_path = get_file_path(filename)
    """Load JSON data from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")  # Debug print
        return {}  # Return an empty structure if the file doesn't exist
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{filename}': {e}")  # Debug print
        return {}  # Return an empty structure if JSON is invalid
def save_json_file(filename, data):
    file_path = get_file_path(filename)
    """Save data to a JSON file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def load_quiz():
    """Load quiz categories from a JSON file."""
    data = load_json_file('qcm.json')
    return data.get("categories", [])

def store_quiz_history(user_id, category, user_answers, score, filename):
    """Store the user's quiz results in the history file."""
    file_path = get_file_path(filename)
    history_data = load_json_file('history.json') or []
    history_id = len(history_data) + 1
    quiz_entry = {
        "id": history_id,
        "user_id": user_id,
        "category": category,
        "questions": user_answers,
        "score": score,
        "date": str(datetime.datetime.now())
    }
    history_data.append(quiz_entry)
    save_json_file('history.json', history_data)

def run_quiz(user_id, category):
    """Run the quiz for a selected category."""
    questions = category.get('questions', [])
    if not questions:
        print("No questions available in this category.")
        return

    random.shuffle(questions)
    score = 0
    user_answers = []

    # Ask how many questions the user wants to attempt
    while True:
        try:
            num_questions = int(input("How many questions would you like to attempt? (10, 20, 30): "))
            if num_questions in [10, 20, 30]:
                break
            print("Invalid number! Please select 10, 20, or 30.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Calculating total time for the quiz
    total_time = num_questions * 20
    print(f"You have {total_time} seconds to complete the quiz.")

    # Start the timer
    start_time = time.time()

    selected_questions = questions[:num_questions]
    for i, question in enumerate(selected_questions, 1):
        elapsed_time = time.time() - start_time
        remaining_time = total_time - elapsed_time

        if remaining_time <= 0:
            print("\nTime is up! The quiz has ended.")
            break

        print(f"\nTime remaining: {int(remaining_time)} seconds")
        print(f"\nQuestion {i}: {question.get('question', 'No question available.')}")

        # Display available options
        for option in question.get('options', []):
            print(f"{option['id']}) {option['text']}")

        # Get valid user input for the answer (a, b, c, or d)
        while True:
            answer = input("Your answer (a/b/c/d): ").lower().strip()
            if answer in ['a', 'b', 'c', 'd']:
                break
            print("Invalid answer! Please choose from a, b, c, or d.")

        # Check if the answer is correct
        is_correct = (answer == question.get('correct_answer', ''))
        user_answers.append({
            "question": question['question'],
            "user_answer": answer,
            "is_correct": is_correct
        })

        if is_correct:
            print("Correct!")
            score += 1
        else:
            correct_answer = next((opt['text'] for opt in question['options'] if opt['id'] == question['correct_answer']), "Unknown")
            print(f"Wrong! The correct answer was: {correct_answer}")

        print(f"Current score: {score}/{i}")

    elapsed_time = time.time() - start_time
    if elapsed_time < total_time:
        print(f"\nQuiz finished! Your final score is {score}/{num_questions}")
    else:
        print(f"\nTime is up! Your final score is {score}/{num_questions}")
        
    store_quiz_history(user_id, category['name'], user_answers, f"{score}/{num_questions}",'history.json')

def start_quiz(username):
    """Start the quiz for a user."""
    user_id = uf.get_user_id(username, 'users.json')
    if not user_id:
        print("Invalid user.")
        return

    categories = load_quiz()
    if not categories:
        print("No quiz data available.")
        return

    print("\nAvailable Categories:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category['name']}")

    # Ask for category choice
    while True:
        try:
            category_choice = int(input("\nChoose a category by number: "))
            if 1 <= category_choice <= len(categories):
                break
            print("Invalid choice!")
        except ValueError:
            print("Please select a valid category number.")

    selected_category = categories[category_choice - 1]
    run_quiz(user_id, selected_category)

    # Ask if the user wants to play again
    while True:
        play_again = input("\nWould you like to play again? (yes/no): ").lower().strip()
        if play_again in ["yes", "no"]:
            break
        print("Invalid input. Please enter 'yes' or 'no'.")

    if play_again == "yes":
        start_quiz(username)
    else:
        print("Thank you for playing! See you next time.")