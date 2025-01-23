import streamlit as st
import datetime
import quiz_app as qa
import user_functions as uf

def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False   # Tracks user login status and tmedelha true if logged in
    if 'username' not in st.session_state:
        st.session_state.username = None     # Stores current username tae user
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False    # Tracks if admin login
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0   # Tracks current question index, there are many usage of it obv
    if 'score' not in st.session_state:
        st.session_state.score = 0      # Stores current qcm score of player
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = []      # Stores user answers for history
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False       # Tracks if quiz is in progress
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = None       # Stores selected qcm category

def display_quiz(category, user_id):

     # check and valid if category has questions
    if not category or not category.get('questions'):
        st.warning("No questions available in this category.")
        return
    
    # Add custom CSS for uniform button width, and answer status colors
    st.markdown("""
        <style>
        .stButton > button {
            width: 100%;
            white-space: normal;
            height: auto;
            min-height: 45px;
        }
        .correct-answer {
            text-align: center;
            background-color: #90EE90 !important;  
            color: #006400 !important;  
            width: 100%;
            padding: 10px;
            border-radius: 5px;
            margin: 5px 0;
            border: 1px solid #ccc;
        }
        .wrong-answer {
            text-align: center;
            background-color: #FFB6C1 !important; 
            color: #8B0000 !important;  
            width: 100%;
            padding: 10px;
            border-radius: 5px;
            margin: 5px 0;
            border: 1px solid #ccc;

        }
        .normal-answer {
            text-align: center;    
            width: 100%;
            padding: 10px;
            border-radius: 5px;
            margin: 5px 0;
            border: 1px solid #ccc;
        }
        </style>
    """, unsafe_allow_html=True)

    # qcm initialization interface
    if not st.session_state.quiz_started:
        st.subheader("Quiz Settings")
        num_questions = st.selectbox(
            "How many questions would you like to attempt?",
            options=[10, 20, 30]
        )
        
        if st.button("Start Quiz"):
            # Initialize qcm with random questions from category
            questions = category.get('questions', [])
            import random
            selected_questions = random.sample(
                questions, 
                min(num_questions, len(questions))
            )
            # Setting states for qcm
            st.session_state.questions = selected_questions
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.user_answers = []
            st.session_state.quiz_started = True
            st.session_state.start_time = datetime.datetime.now()
            st.session_state.total_time = num_questions * 10# 10 seconds per question, change here if you want to test the time
            st.session_state.answer_submitted = False
            st.session_state.quiz_completed = False  # status added to prevent multiple history entries, we'll try and see hopefully it works (it worked yay)
            st.rerun()
    
    # qcm running interface
    elif st.session_state.quiz_started:
        st.empty()
        
        questions = st.session_state.questions
        current_q = st.session_state.current_question
        
        # Calculate remaining time by seconds
        elapsed_time = (datetime.datetime.now() - st.session_state.start_time).total_seconds()
        remaining_time = max(0, st.session_state.total_time - elapsed_time)
        
        # Display qcm header with question number, score, and time
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            if current_q < len(questions):
                st.subheader(f"Question {current_q + 1}")
            else:
                st.subheader(f"Question {len(questions)}")  # Ensure it remains at the total number of questions after displaying the last question
        with col2:
            st.subheader(f"Score: {st.session_state.score}")
        with col3:
            st.subheader(f"Time: {int(remaining_time)}s")
        
        # Display progress bar (pretty innit)
        progress = st.progress((current_q) / len(questions))
        
        # Handle qcm timeout
        if remaining_time <= 0:
            st.error("Time's up! Quiz ended.")
            
            # Store qcm history in cas user didn't make it in time 
            if not st.session_state.get('quiz_completed', False):
                final_score = st.session_state.score
                total_questions = len(questions)
                
                qa.store_quiz_history(
                    user_id,
                    category['name'],
                    st.session_state.user_answers,
                    f"{final_score}/{total_questions}",
                    'history.json'
                )
                st.session_state.quiz_completed = True
            
            # Show final score and a cta to ask if user wants to take another try
            st.success(f"Quiz completed! Your score: {st.session_state.score}/{len(questions)}")
            
            if st.button("Take Another Quiz"):
                # Reset qcm states
                st.session_state.quiz_started = False
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.user_answers = []
                st.session_state.selected_category = None
                st.session_state.quiz_completed = False
                st.rerun()
            return
        
        # Display current question and options
        if current_q < len(questions):
            question = questions[current_q]
            
            st.write("---")
            st.write(question['question'])
            
            col1, col2 = st.columns(2)
            
            # Show options if answer not submitted
            if not st.session_state.get('answer_submitted', False):
                for idx, opt in enumerate(question['options']):
                    with col1 if idx < 2 else col2:
                        if st.button(f"{opt['id']}) {opt['text']}", key=f"opt_{opt['id']}"):
                            st.session_state.selected_answer = opt['id']
                            st.session_state.answer_submitted = True
                            st.rerun()
            
            # Show the correct and wrong answers by colors
            else:
                for idx, opt in enumerate(question['options']):
                    with col1 if idx < 2 else col2:
                        if opt['id'] == question['correct_answer']:
                            css_class = "correct-answer"
                        elif opt['id'] == st.session_state.selected_answer:
                            css_class = "wrong-answer" if opt['id'] != question['correct_answer'] else "correct-answer"
                        else:
                            css_class = "normal-answer"

                        # Display the option with appropriate styling colors
                        st.markdown(
                            f'<div class="{css_class}">{opt["id"]}) {opt["text"]}</div>',
                            unsafe_allow_html=True
                        )
                
                # Handle next question 
                if st.button("Next Question"):
                    is_correct = (st.session_state.selected_answer == question['correct_answer'])
                    if is_correct:
                        st.session_state.score += 1
                    
                    # Store answer for history
                    st.session_state.user_answers.append({
                        "question": question['question'],
                        "user_answer": st.session_state.selected_answer,
                        "is_correct": is_correct
                    })
                    
                    st.session_state.current_question += 1
                    st.session_state.answer_submitted = False
                    st.rerun()
        
        # Qcm completed
        else:
            # Only store qcm history if it hasn't been stored yet
            if not st.session_state.get('quiz_completed', False):
                final_score = st.session_state.score
                total_questions = len(questions)
                
                qa.store_quiz_history(
                    user_id,
                    category['name'],
                    st.session_state.user_answers,
                    f"{final_score}/{total_questions}",
                    'history.json'
                )
                st.session_state.quiz_completed = True  # Mark quiz as completed
            
            st.success(f"Quiz completed! Your score: {st.session_state.score}/{len(questions)}")
            
            # Option to start new qcm
            if st.button("Take Another Quiz"):
                st.session_state.quiz_started = False
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.user_answers = []
                st.session_state.selected_category = None
                st.session_state.quiz_completed = False  # Reset completion status
                st.rerun()

def view_history(user_id):
    try:
        history_data = qa.load_json_file('history.json')
        if not history_data:
            st.warning("No history available.")
            return

        # Filter history for current user    
        user_history = [game for game in history_data if game['user_id'] == user_id]

        if user_history:
            st.subheader("Your Quiz History")
            # Display each qcm attempt with questions and answers
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
    except Exception as e:
        st.error(f"Error loading history: {str(e)}")

def admin_menu():
    st.title("Admin Menu")
    
    menu_choice = st.sidebar.radio(
        "Admin Options",
        ["Add Category", "Add Question", "Delete Category", "Delete Question", "Logout"]
    )
    
    # Adding new category
    if menu_choice == "Add Category":
        st.subheader("Add New Category")
        category_name = st.text_input("Enter category name:")
        if st.button("Add Category") and category_name:
            data = qa.load_json_file('questions.json') or {"categories": []}
            
            # Check if category exists
            if any(cat["name"].lower() == category_name.lower() for cat in data["categories"]):
                st.error("Category already exists!")
            else:
                new_category_id = 1 if not data["categories"] else data["categories"][-1]["id"] + 1
                new_category = {
                    "id": new_category_id,
                    "name": category_name,
                    "questions": []
                }
                data["categories"].append(new_category)
                qa.save_json_file('questions.json', data)
                st.success(f"Category '{category_name}' added successfully!")

    # Adding new question
    elif menu_choice == "Add Question":
        st.subheader("Add Question")
        
        # Load categories for selection
        data = qa.load_json_file('questions.json') or {"categories": []}
        categories = data.get("categories", [])
        
        if not categories:
            st.warning("No categories available. Please create a category first.")
            return
            
        # Category selection
        category_names = [cat["name"] for cat in categories]
        selected_category = st.selectbox("Select Category:", category_names)
        
        # Question input form
        with st.form("add_question_form"):
            question_text = st.text_input("Enter question:")
            option_a = st.text_input("Option A:")
            option_b = st.text_input("Option B:")
            option_c = st.text_input("Option C:")
            option_d = st.text_input("Option D:")
            correct_answer = st.selectbox("Correct Answer:", ["a", "b", "c", "d"])
            
            submit_button = st.form_submit_button("Add Question")
            
            if submit_button:
                if not all([question_text, option_a, option_b, option_c, option_d]):
                    st.error("Please fill in all fields!")
                else:
                    # Find selected category and add question
                    category = next(cat for cat in categories if cat["name"] == selected_category)
                    
                    # Create new question
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
                    
                    # Add question to category
                    category["questions"].append(new_question)
                    qa.save_json_file('questions.json', data)
                    st.success("Question added successfully!")

    # Deleting category
    elif menu_choice == "Delete Category":
        st.subheader("Delete Category")
        
        # Load categories
        data = qa.load_json_file('questions.json') or {"categories": []}
        categories = data.get("categories", [])
        
        if not categories:
            st.warning("No categories available.")
            return
        
        # Display categories with their questions count
        category_options = [f"{cat['name']} ({len(cat['questions'])} questions)" for cat in categories]
        selected_category = st.selectbox("Select category to delete:", category_options)
        
        if st.button("Delete Category"):
            category_name = selected_category.split(" (")[0]
            data["categories"] = [cat for cat in categories if cat["name"] != category_name]
            qa.save_json_file('questions.json', data)
            st.success(f"Category '{category_name}' deleted successfully!")

    elif menu_choice == "Delete Question":
        st.subheader("Delete Question")
        
        # Load categories
        data = qa.load_json_file('questions.json') or {"categories": []}
        categories = data.get("categories", [])
        
        if not categories:
            st.warning("No categories available.")
            return
        
        # Category selection
        category_names = [cat["name"] for cat in categories]
        selected_category_name = st.selectbox("Select Category:", category_names)
        
        # Get selected category and its questions
        category = next(cat for cat in categories if cat["name"] == selected_category_name)
        questions = category.get("questions", [])
        
        if not questions:
            st.warning("No questions available in this category.")
            return
        
        # Question selection
        question_options = [f"Q{q['id']}: {q['question']}" for q in questions]
        selected_question = st.selectbox("Select question to delete:", question_options)
        
        if st.button("Delete Question"):
            question_id = int(selected_question.split(":")[0][1:])
            category["questions"] = [q for q in questions if q["id"] != question_id]
            qa.save_json_file('questions.json', data)
            st.success("Question deleted successfully!")
    
    elif menu_choice == "Logout":
        if st.button("Confirm Logout"):
            st.session_state.is_admin = False
            st.rerun()

def main():
    init_session_state()
    
    if not st.session_state.logged_in and not st.session_state.is_admin:
        st.title("Quiz Application")
        login_tab, register_tab, admin_tab = st.tabs(["User Login", "Register", "Admin Login"])
        
        with login_tab:
            username = st.text_input("Username", key="user_username")
            password = st.text_input("Password", type="password", key="user_password")
            
            if st.button("Login", key="user_login"):
                if uf.login(username, password, 'users.json'):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid username or password!")
        
        with register_tab:
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            
            if st.button("Register"):
                if uf.user_exists(new_username, 'users.json'):
                    st.error("Username already exists!")
                else:
                    uf.add_user(new_username, new_password, 'users.json')
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
                if not st.session_state.quiz_started:
                    selected_category = st.selectbox(
                        "Choose a category:",
                        categories,
                        format_func=lambda x: x['name']
                    )
                    if selected_category:
                        st.session_state.selected_category = selected_category
                
                if st.session_state.selected_category:
                    display_quiz(
                        st.session_state.selected_category,
                        uf.get_user_id(st.session_state.username, 'users.json')
                    )
            else:
                st.warning("No quiz data available.")
        
        elif menu_choice == "View History":
            view_history(uf.get_user_id(st.session_state.username, 'users.json'))
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