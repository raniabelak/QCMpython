# QCMpython

Welcome! 

This project provides a fun and interactive way to take quizzes and manage quiz data through an easy interface powered by Streamlit.

---

## Features

- **User-Friendly Interface:**
  - User login and registration.
  - Admin login for managing quizzes.

- **Quiz Features:**
  - Select categories and set the number of questions.
  - Timer and progress tracking.
  - Immediate score calculation and answer review.

- **Admin Functionalities:**
  - Add, delete categories and questions.
  - Manage quiz data efficiently.

- **History Tracking:**
  - View previous quiz attempts and scores.

---

## Requirements

- **Python 3.7+**
- Libraries:
  - `streamlit`
  - `json`
  - `datetime`
  - `time`
  - `random`

---

## Installation

1. **Clone the Repository:**
   You need to clone this repository first so you can run this project

2. **Install Dependencies:**
   Before starting, you need to install the streamlit library, it's very easy and simple, all you have to do is running this command in cmd, don't forget to **run is as administrator**:
   ```bash
   pip install streamlit
   ```
   After installation, verify by running the following command:
   ```bash
   pip show streamlit
   ```

3. **Run the Application:**
   Finally, to start the Streamlit application, use the command:
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Access the App:**
   Open your browser and navigate to the URL shown in your terminal (usually `http://localhost:8501`).

---

## How to Use

### For Users

1. **Login or Register:**
   - Open the app and either log in with your existing credentials or register as a new user.

2. **Take a Quiz:**
   - Select the "Take Quiz" option from the sidebar.
   - Choose a category and configure your quiz settings.
   - Answer the questions within the time limit, initially you will get 10 seconds per questions.

3. **Results & Feedbacks:**
   - After completing each question of quiz, view your score and review the correct and incorrect answers by checking the styling colors (red if answer incorrect, green if answer correct).

4. **View History:**
   - Use the "View History" option to see your past quiz attempts.

### For Admins

1. **Login as Admin:**
   - Enter the admin code (default: `admin2025`) in the admin login tab.

2. **Manage Quizzes:**
   - Use the admin menu to add or delete categories and questions. (the qcm/quiz questions are modified in questions.json instead of qcm.json, to verify the data manipulation and ensure that the user doesn't delete from our main collected quiz questions in qcm.json)
   - Ensure questions have clear options and a correct answer specified.

3. **Logout:**
   - Use the "Logout" option to exit admin mode securely.

---

## Notes

- Ensure you have the `questions.json` and `users.json` files in the same directory as the app for proper functionality.
- The app stores user and quiz data in JSON format. Handle these files carefully to avoid data loss.

---

## Troubleshooting

- **Streamlit Command Not Found:** Ensure Streamlit is installed by running:
  ```bash
  pip install streamlit
  ```

- **Port Issues:** If the default port `8501` is busy, specify a new port:
  ```bash
  streamlit run streamlit_app.py --server.port=8502
  ```

---

Thank you for using our app, enjoy!
