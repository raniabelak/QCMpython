import streamlit as st
import json
import datetime
from user_functions import user_exists, add_user, login, get_user_id
import admin_functions as af
import quiz_app as qa

# Initialize session state variables to ensure default values are set for the user's session.

def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = []
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = None

# Handles the quiz display and logic (starting the quiz,navigating questions,tracking the user's progress)

def display_quiz(category, user_id):
    if not category or not category.get('questions'):
        st.warning("No questions available in this category.")
        return

    if not st.session_state.quiz_started:
        st.subheader("Quiz Settings")
        num_questions = st.selectbox(
            "How many questions would you like to attempt?",
            options=[10, 20, 30]
        )
        
        if st.button("Start Quiz"):
            questions = category.get('questions', [])
            import random
            selected_questions = random.sample(
                questions, 
                min(num_questions, len(questions))
            )
            st.session_state.questions = selected_questions
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.user_answers = []
            st.session_state.quiz_started = True
            # Initialize timer-related session states
            st.session_state.start_time = datetime.datetime.now()
            st.session_state.total_time = num_questions * 10  # 10 seconds per question
            st.rerun()
    
    elif st.session_state.quiz_started:
        # Clear the settings page content, i added it + it states to avoid displaying the settings after the quiz has started
        st.empty()
        
        questions = st.session_state.questions
        current_q = st.session_state.current_question
        
        # Calculate remaining time
        elapsed_time = (datetime.datetime.now() - st.session_state.start_time).total_seconds()
        remaining_time = max(0, st.session_state.total_time - elapsed_time)
        
        # Create three columns for the header
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.subheader(f"Question {current_q + 1}")
        with col2:
            st.subheader(f"Score: {st.session_state.score}")
        with col3:
            st.subheader(f"Time: {int(remaining_time)}s")
        
        # Display progress
        progress = st.progress((current_q) / len(questions))
        
        # Check if time is up
        if remaining_time <= 0:
            st.error("Time's up! Quiz ended.")
            st.session_state.current_question = len(questions)  # Skip to the end of the quiz
            st.rerun()
            return
        
        if current_q < len(questions):
            question = questions[current_q]
            
            st.write("---")
            st.write(question['question'])
            
            # Displaying options (currently radio buttons, may change to checkboxes)
            options = {opt['id']: opt['text'] for opt in question['options']}
            answer = st.radio(
                "Choose your answer:",
                options.keys(),
                format_func=lambda x: f"{x}) {options[x]}"
            )
            
            # Create columns for navigation buttons
            col1, col2 = st.columns([1, 5])
            
            with col1:
                if st.button("Next Question"):
                    is_correct = (answer == question['correct_answer'])
                    if is_correct:
                        st.session_state.score += 1
                    
                    st.session_state.user_answers.append({
                        "question": question['question'],
                        "user_answer": answer,
                        "is_correct": is_correct
                    })
                    
                    st.session_state.current_question += 1
                    st.rerun()
        
        else:
            # Quiz finished
            final_score = st.session_state.score
            total_questions = len(questions)
            
            st.success(f"Quiz completed! Your score: {final_score}/{total_questions}")
            
            # Store the quiz history (used from quiz_app.py file)
            qa.store_quiz_history(
                user_id,
                category['name'],
                st.session_state.user_answers,
                f"{final_score}/{total_questions}"
            )
            
            # Display the full answers
            st.subheader("Review Your Answers")
            for i, (q, a) in enumerate(zip(questions, st.session_state.user_answers)):
                correct_ans = next(opt['text'] for opt in q['options'] if opt['id'] == q['correct_answer'])
                user_ans = next(opt['text'] for opt in q['options'] if opt['id'] == a['user_answer'])
                
                st.write(f"**Question {i+1}:** {q['question']}")
                st.write(f"Your answer: {user_ans}")
                st.write(f"Correct answer: {correct_ans}")
                if a['is_correct']:
                    st.success("Correct! ✅")
                else:
                    st.error("Incorrect ❌")
                st.write("---")
            
            if st.button("Take Another Quiz"):
                st.session_state.quiz_started = False
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.user_answers = []
                st.session_state.selected_category = None
                st.rerun()

# Display the quiz history for a specific user, including their answers, scores, and dates

def view_history(user_id):
    try:
        with open('history.json', 'r', encoding='utf-8') as file:
            history_data = json.load(file)
    except FileNotFoundError:
        st.warning("No history available.")
        return
    except json.JSONDecodeError:
        st.error("Error reading history data.")
        return

    if not isinstance(history_data, list):
        st.error("Invalid history data format.")
        return

# The ID of the logged-in user in user_id
    user_history = [game for game in history_data if game['user_id'] == user_id]

    if user_history:
        st.subheader("Your Quiz History")
        for index, game in enumerate(user_history, start=1):
            with st.expander(f"Game {index}: {game['category']} - Score: {game['score']} - Date: {game['date']}"):
                st.write("Questions and Answers:")
                for q in game['questions']:
                    st.write(f"Question: {q['question']}")
                    st.write(f"Your answer: {q['user_answer']}")
                    if q['is_correct']:
                        st.success("Correct ✅")
                    else:
                        st.error("Incorrect ❌")
                    st.write("---")
    else:
        st.info("No quiz history found.")

# I added this fct for admin functionalities (adding/deleting categories and questions, anf ofc logging out of the admin account

def admin_menu():
    st.title("Admin Menu")
    
    menu_choice = st.sidebar.radio(
        "Admin Options",
        ["Add Category/Question", "Delete Category", "Delete Question", "Logout"]
    )
    
    if menu_choice == "Add Category/Question":
        st.subheader("Add New Category or Question")
        # Input for category
        category_name = st.text_input("Enter category name:").strip()
        
        if st.button("Create/Select Category") and category_name:
            try:
                with open('questions.json', 'r', encoding='utf-8') as file:
                    data = json.load(file)
            except FileNotFoundError:
                data = {"categories": []}
            
            # Check if category exists
            category = next((cat for cat in data["categories"] 
                           if cat["name"].lower() == category_name.lower()), None)
            
            if not category:
                # Create new category
                new_category_id = 1 if not data["categories"] else data["categories"][-1]["id"] + 1
                new_category = {
                    "id": new_category_id,
                    "name": category_name,
                    "questions": []
                }
                data["categories"].append(new_category)
                with open('questions.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=2, ensure_ascii=False)
                st.success(f"Created new category '{category_name}'")
            else:
                st.info(f"Category '{category_name}' already exists")
            
            st.session_state.current_category = category_name
        
        # Add question form
        if 'current_category' in st.session_state:
            st.subheader("Add Question")
            with st.form("add_question"):
                question_text = st.text_input("Question:")
                option_a = st.text_input("Option A:")
                option_b = st.text_input("Option B:")
                option_c = st.text_input("Option C:")
                option_d = st.text_input("Option D:")
                correct_answer = st.selectbox(
                    "Correct Answer:",
                    ["a", "b", "c", "d"]
                )
                
                if st.form_submit_button("Add Question"):
                    with open('questions.json', 'r', encoding='utf-8') as file:
                        data = json.load(file)
                    
                    category = next((cat for cat in data["categories"] 
                                  if cat["name"].lower() == st.session_state.current_category.lower()), None)
                    
                    if category:
                        question_id = len(category["questions"]) + 1
                        new_question = {
                            "id": question_id,
                            "question": question_text,
                            "options": [
                                {"id": "a", "text": option_a},
                                {"id": "b", "text": option_b},
                                {"id": "c", "text": option_c},
                                {"id": "d", "text": option_d}
                            ],
                            "correct_answer": correct_answer
                        }
                        category["questions"].append(new_question)
                        
                        with open('questions.json', 'w', encoding='utf-8') as file:
                            json.dump(data, file, indent=2, ensure_ascii=False)
                        st.success("Question added successfully!")
    
    elif menu_choice == "Delete Category":
        st.subheader("Delete Category")
        try:
            with open('questions.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            if data["categories"]:
                categories = [f"{cat['id']}. {cat['name']}" for cat in data["categories"]]
                selected = st.selectbox("Select category to delete:", categories)
                
                if st.button("Delete Category"):
                    category_id = int(selected.split('.')[0])
                    data["categories"] = [cat for cat in data["categories"] if cat["id"] != category_id]
                    
                    with open('questions.json', 'w', encoding='utf-8') as file:
                        json.dump(data, file, indent=2, ensure_ascii=False)
                    st.success("Category deleted successfully!")
            else:
                st.info("No categories available.")
        except FileNotFoundError:
            st.error("Questions file not found.")
    
    elif menu_choice == "Delete Question":
        st.subheader("Delete Question")
        try:
            with open('questions.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            if data["categories"]:
                categories = [f"{cat['id']}. {cat['name']}" for cat in data["categories"]]
                selected_category = st.selectbox("Select category:", categories)
                category_id = int(selected_category.split('.')[0])
                
                category = next((cat for cat in data["categories"] if cat["id"] == category_id), None)
                if category and category["questions"]:
                    questions = [f"{q['id']}. {q['question']}" for q in category["questions"]]
                    selected_question = st.selectbox("Select question to delete:", questions)
                    
                    if st.button("Delete Question"):
                        question_id = int(selected_question.split('.')[0])
                        category["questions"] = [q for q in category["questions"] if q["id"] != question_id]
                        
                        with open('questions.json', 'w', encoding='utf-8') as file:
                            json.dump(data, file, indent=2, ensure_ascii=False)
                        st.success("Question deleted successfully!")
                else:
                    st.info("No questions available in this category.")
            else:
                st.info("No categories available.")
        except FileNotFoundError:
            st.error("Questions file not found.")
    
    elif menu_choice == "Logout":
        if st.button("Confirm Logout"):
            st.session_state.is_admin = False
            st.rerun()

# Main entry function to handle the login/register process, user menu, and admin menu

def main():
    init_session_state()
    
    if not st.session_state.logged_in and not st.session_state.is_admin:
        st.title("Login/Register")
        login_tab, register_tab, admin_tab = st.tabs(["User Login", "Register", "Admin Login"])
        
        with login_tab:
            username = st.text_input("Username", key="user_username")
            password = st.text_input("Password", type="password", key="user_password")
            
            if st.button("Login", key="user_login"):
                if login(username, password, 'users.json'):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid username or password!")
        
        with register_tab:
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            
            if st.button("Register"):
                if user_exists(new_username, 'users.json'):
                    st.error("Username already exists!")
                else:
                    add_user(new_username, new_password, 'users.json')
                    st.success("Registration successful! Please login.")

        with admin_tab:
            admin_code = st.text_input("Admin Code", type="password", key="admin_code")
            if st.button("Admin Login", key="admin_login"):
                if admin_code.lower() == "admin2025":
                    st.session_state.is_admin = True
                    st.rerun()
                else:
                    st.error("Invalid admin code!")
    
    elif st.session_state.is_admin:
        admin_menu()
    
    elif st.session_state.logged_in:
        st.title(f"Welcome, {st.session_state.username}!")
        
        menu_choice = st.sidebar.radio(
            "Menu",
            ["Take Quiz", "View History", "Logout"]
        )
        
        if menu_choice == "Take Quiz":
            categories = qa.load_quiz()
            if categories:
                # Only show category selection if quiz hasn't started
                if not st.session_state.quiz_started:
                    selected_category = st.selectbox(
                        "Choose a category:",
                        categories,
                        format_func=lambda x: x['name']
                    )
                    if selected_category:
                        st.session_state.selected_category = selected_category
                
                # Use the stored category for the quiz
                if st.session_state.selected_category:
                    display_quiz(st.session_state.selected_category, get_user_id(st.session_state.username))
            else:
                st.warning("No quiz data available.")
        
        elif menu_choice == "View History":
            view_history(get_user_id(st.session_state.username))
            # Reset quiz state when viewing history (to avoid conflicts)
            st.session_state.quiz_started = False
            st.session_state.selected_category = None
        
        elif menu_choice == "Logout":
            if st.button("Confirm Logout"):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.quiz_started = False
                st.session_state.selected_category = None
                st.rerun()

if __name__ == "__main__":
    main()