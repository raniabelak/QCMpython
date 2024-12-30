import json
import random
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def load_quiz_data(filename='qcm.json'):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            quiz_data = json.load(file)
            return quiz_data["categories"]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return []

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("800x600")

        self.categories = load_quiz_data()
        self.selected_category = None
        self.num_questions = 10
        self.current_question_index = 0
        self.score = 0
        self.questions = []

        self.home_screen()

    def home_screen(self):
        self.clear_screen()

        ttk.Label(self.root, text="Welcome to the Quiz App!", font=("Arial", 24), bootstyle=PRIMARY).pack(pady=20)

        if not self.categories:
            ttk.Label(self.root, text="No quiz data available. Please check your JSON file.", font=("Arial", 16), bootstyle=DANGER).pack(pady=20)
            return

        ttk.Label(self.root, text="Select Category:", font=("Arial", 14)).pack(pady=10)
        self.category_var = ttk.StringVar(value=self.categories[0]["name"])
        category_menu = ttk.Combobox(self.root, textvariable=self.category_var, values=[cat["name"] for cat in self.categories], font=("Arial", 12))
        category_menu.pack(pady=10)

        ttk.Label(self.root, text="Number of Questions:", font=("Arial", 14)).pack(pady=10)
        self.question_var = ttk.IntVar(value=10)
        question_menu = ttk.Combobox(self.root, textvariable=self.question_var, values=[10, 20, 30], font=("Arial", 12))
        question_menu.pack(pady=10)

        ttk.Button(self.root, text="Start Quiz", bootstyle=SUCCESS, command=self.start_quiz).pack(pady=20)

    def start_quiz(self):
        category_name = self.category_var.get()
        self.num_questions = self.question_var.get()
        self.selected_category = next(cat for cat in self.categories if cat["name"] == category_name)
        self.questions = random.sample(self.selected_category['questions'], self.num_questions)
        self.current_question_index = 0
        self.score = 0

        self.question_screen()

    def question_screen(self):
        self.clear_screen()

        if self.current_question_index >= len(self.questions):
            self.result_screen()
            return

        question = self.questions[self.current_question_index]
        ttk.Label(self.root, text=f"Question {self.current_question_index + 1}/{self.num_questions}", font=("Arial", 16)).pack(pady=10)
        ttk.Label(self.root, text=question["question"], font=("Arial", 14), wraplength=600).pack(pady=20)

        self.answer_var = ttk.StringVar(value="")
        for option in question["options"]:
            ttk.Radiobutton(self.root, text=option["text"], value=option["id"], variable=self.answer_var, bootstyle=INFO).pack(anchor="w", padx=50)

        ttk.Button(self.root, text="Next", bootstyle=SUCCESS, command=self.check_answer).pack(pady=20)

    def check_answer(self):
        selected_answer = self.answer_var.get()
        correct_answer = self.questions[self.current_question_index]["correct_answer"]

        if selected_answer == correct_answer:
            self.score += 1

        self.current_question_index += 1
        self.question_screen()

    def result_screen(self):
        self.clear_screen()

        percentage = (self.score / self.num_questions) * 100
        ttk.Label(self.root, text="Quiz Completed!", font=("Arial", 24), bootstyle=PRIMARY).pack(pady=20)
        ttk.Label(self.root, text=f"Final Score: {self.score}/{self.num_questions}", font=("Arial", 18)).pack(pady=10)
        ttk.Label(self.root, text=f"Percentage: {percentage:.1f}%", font=("Arial", 18)).pack(pady=10)

        if percentage == 100:
            message = "Perfect score! You're an expert!"
        elif percentage >= 80:
            message = "Great job! You really know a lot!"
        elif percentage >= 60:
            message = "Good effort! Keep learning!"
        else:
            message = "Keep practicing! You'll get better!"

        ttk.Label(self.root, text=message, font=("Arial", 16), bootstyle=SUCCESS).pack(pady=20)

        ttk.Button(self.root, text="Play Again", bootstyle=INFO, command=self.home_screen).pack(pady=10)
        ttk.Button(self.root, text="Exit", bootstyle=DANGER, command=self.root.destroy).pack(pady=10)

    # Clear Screen
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = ttk.Window(themename="flatly")  
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
