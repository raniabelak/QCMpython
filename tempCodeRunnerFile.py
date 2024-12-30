import json
import random


# Load quiz data from the JSON file
def load_quiz(filename='qcm.json'):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            quiz_data = json.load(file)
            return quiz_data["categories"]
    except FileNotFoundError:
        print("Error: The quiz file does not exist.")
        return []
    except json.JSONDecodeError:
        print("Error: Failed to decode the quiz file. Please check the JSON format.")
        return []


# Select a category for the quiz
def select_category(categories):
    print("\nAvailable categories:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category['name']}")
    
    while True:
        try:
            category_choice = int(input("\nChoose a category (1 to {0}): ".format(len(categories))))
            if 1 <= category_choice <= len(categories):
                return categories[category_choice - 1]
            else:
                print("Invalid choice! Please select a valid category number.")
        except ValueError:
            print("Invalid input! Please enter a number.")


# Run the quiz for a selected category
def run_quiz(category):
    questions = category['questions']

    # Ask the user for the number of questions
    while True:
        try:
            num_questions = int(input("\nHow many questions would you like to attempt? (10, 20, 30): "))
            if num_questions in [10, 20, 30]:
                break
            else:
                print("Invalid choice! Please enter 10, 20, or 30.")
        except ValueError:
            print("Invalid input! Please enter a number.")

    # Shuffle and select the requested number of questions
    random.shuffle(questions)
    questions = questions[:num_questions]
    score = 0
    total_questions = len(questions)

    print(f"\nWelcome to the {category['name']} Quiz!")
    print("============================")

    for i, q in enumerate(questions, 1):
        print(f"\nQuestion {i}/{total_questions}:")
        print(q["question"])

        # Display options
        for option in q["options"]:
            print(f"{option['id']}) {option['text']}")

        # Get user's answer
        while True:
            answer = input("\nYour answer (a/b/c/d): ").lower().strip()
            if answer in ['a', 'b', 'c', 'd']:
                break
            print("Invalid input! Please enter a, b, c, or d.")

        # Verify answer
        if answer == q["correct_answer"]:
            print("\nCorrect answer!")
            score += 1
        else:
            correct_text = next(opt["text"] for opt in q["options"] if opt["id"] == q["correct_answer"])
            print(f"\nWrong answer! The correct answer was: {correct_text}")

        print(f"Current score: {score}/{i}")

    # Display final results
    percentage = (score / total_questions) * 100
    print("\n============================")
    print("QCM completed!")
    print(f"Final score: {score}/{total_questions}")
    print(f"Percentage: {percentage:.1f}%")

    # Add motivational messages based on score
    if percentage == 100:
        print("Perfect score! You're an expert!")
    elif percentage >= 80:
        print("Great job! You really know Alot !")
    elif percentage >= 60:
        print("Good effort! Keep learning!")
    else:
        print("Keep practicing! You'll get better!")


# Main loop to run the quiz
def main():
    categories = load_quiz()
    if not categories:
        print("Unable to load quiz data. Exiting the program.")
        return

    while True:
        selected_category = select_category(categories)
        run_quiz(selected_category)

        play_again = input("\nPlay again? (yes/no): ").lower().strip()
        if play_again != 'yes':
            print("\nThanks for playing! Goodbye!")
            break


if __name__ == "__main__":
    main()
