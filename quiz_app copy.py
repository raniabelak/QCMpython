import json
import random
import datetime
import user_functions as uf

# Function to load a JSON file
def load_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {file_path}: {e}")
        return {}

# Function to save a JSON file
def save_file(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving file {file_path}: {e}")

# Function to load quiz categories
def load_quiz():
    categories_data = load_file('qcm.json')
    return categories_data.get("categories", [])

# Function to store the user's quiz results in the history file
def store_quiz_history(user_id, category, user_answers, score):
    history_data = load_file('history.json') or []
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
    save_file('history.json', history_data)

# Function to run the quiz
def run_quiz(user_id, category):
    questions = category.get('questions', [])
    if not questions:
        print("No questions available in this category.")
        return

    random.shuffle(questions)
    score = 0
    user_answers = []

    # Ask how many questions the user wants to attempt
    try:
        num_questions = int(input("How many questions would you like to attempt? (10, 20, 30): "))
        if num_questions not in [10, 20, 30]:
            print("Invalid number! Please select 10, 20, or 30.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    selected_questions = questions[:num_questions]
    for i, question in enumerate(selected_questions, 1):
        print(f"\nQuestion {i}: {question.get('question', 'No question available.')}")

        # Display available options
        for option in question.get('options', []):
            print(f"{option['id']}) {option['text']}")

        # Get valid user input for the answer (a, b, c, or d)
        while True:
            answer = input("Your answer (a/b/c/d): ").lower().strip()
            if answer in ['a', 'b', 'c', 'd']:
                break
            else:
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

    print(f"\nQuiz finished! Your final score is {score}/{num_questions}")
    store_quiz_history(user_id, category['name'], user_answers, f"{score}/{num_questions}")

# Main function to start the quiz
def start_quiz(username):
    user_id = uf.get_user_id(username)
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

    try:
        category_choice = int(input("\nChoose a category by number: "))
        if category_choice < 1 or category_choice > len(categories):
            print("Invalid choice!")
            return
    except ValueError:
        print("Please select a valid category number.")
        return

    selected_category = categories[category_choice - 1]
    run_quiz(user_id, selected_category)

    play_again = input("\nWould you like to play again? (yes/no): ").lower().strip()
    if play_again == 'yes':
        start_quiz(username)
    else:
        print("Thank you for playing! See you next time.")