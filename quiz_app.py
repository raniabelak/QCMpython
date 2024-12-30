import json
import random


# Open and read the JSON file
def load_quiz():
    with open('qcm.json', 'r', encoding='utf-8') as file:
        quiz_data = json.load(file)
        return quiz_data["categories"][0]["questions"] # load the questions from the first category


def run_quiz():
    questions = load_quiz()
    score = 0
    total_questions = len(questions) # get the to total number of questions from the JSON file
    
    print("\nWelcome to the Football Quiz!")
    print("============================")
    
    # Shuffle questions for variety (logically it's needed)
    random.shuffle(questions)
    
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
            
            # Find the correct answer directly from the options
            correct_text = next(opt["text"] for opt in q["options"] if opt["id"] == q["correct_answer"])
            print(f"\nWrong answer! The correct answer was: {correct_text}")

            # Dictionary method:
            # correct_text = {opt["id"]: opt["text"] for opt in q["options"]}[q["correct_answer"]]
            # print(f"\nWrong answer! The correct answer was: {correct_text}")

        print(f"Current score: {score}/{i}")
        input("\nPress Enter to continue...")
    
    # Display final results (till now we answer all questions to test, no limit)
    percentage = (score / total_questions) * 100
    print("\n============================")
    print("QCM completed!")
    print(f"Final score: {score}/{total_questions}")
    print(f"Percentage: {percentage:.1f}%")

    # adding printing conditions from nassim JSON test file
    
    if percentage == 100:
        print("Perfect score! You're a football expert!")
    elif percentage >= 80:
        print("Great job! You really know your football!")
    elif percentage >= 60:
        print("Good effort! Keep learning about football!")
    else:
        print("Keep practicing! You'll get better!")

# I have to understand the (if __name__ == "__main__":) part, could be necessary to run in other programs
# if __name__ == "__main__":
#     while True:
#         run_quiz()
#         play_again = input("\nWould you like to try again? (yes/no): ").lower().strip()
#         if play_again != 'yes':
#             print("\nThanks for playing! Goodbye!")
#             break

keep_playing = True
while keep_playing:
    run_quiz()
    play_again = input("\nPlay again? (yes/no): ").lower().strip()
    keep_playing = (play_again == 'yes')

print("\nThanks for playing! Goodbye!")
