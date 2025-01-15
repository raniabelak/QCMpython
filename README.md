# Multiple-Choice Questionnaire (MCQ) Application for Computer Science Students

### Realized by:
- **BELAKEBI Rania** (222231633510)
- **HESSAS Nassim** (222231395417)
- **MAHMOUD Rayan** (22231395305)
- **LAOUDI Farid** (222231327013)

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Data Management](#data-management)
4. [Implementation Details](#implementation-details)
    - [admin_functions.py](#admin_functionspy)
    - [user_functions.py](#user_functionspy)
    - [main.py](#mainpy)
    - [quiz_app.py](#quiz_apypy)
5. [Graphical Interface](#graphical-interface)
6. [Conclusion](#conclusion)

---

## Project Overview

The **Multiple-Choice Questionnaire (MCQ)** Application is a comprehensive tool designed for computer science students. It not only allows users to take quizzes but also provides administrative functionalities for managing quiz content. Developed using Python, this project leverages the simplicity and versatility of the language, with JSON being used for data storage to ensure data persistence across sessions.

### Key Features:
- **User Authentication**: Secure access to the application.
- **Quiz Management**: Allows users to take quizzes and view past performance with history tracking.
- **Admin Functions**: Administrators can add or remove categories and questions dynamically.
- **Data Storage**: Information is stored in structured JSON files (`users.json`, `qcm.json`, `history.json`), which handle user data, quiz questions, and history tracking respectively.

This project stands out due to its modularity, ease of use, and robust data handling capabilities.

---

## System Architecture

The application is structured into different components that separate the responsibilities for a clean and manageable codebase.

- **main.py**: The entry point of the application that handles user authentication and navigates users to their respective interfaces (user or admin).
- **quiz_app.py**: Manages quiz execution, including question presentation, user input handling, and score calculation.
- **admin_functions.py**: Contains administrative functionalities such as adding or deleting quiz categories and questions.
- **user_functions.py**: Handles user management tasks such as registration, login, and authentication.

### Data Files:
- **users.json**: Stores user details, including usernames and passwords.
- **qcm.json**: Contains the categories and questions for quizzes.
- **history.json**: Tracks the history of quiz attempts, including scores, attempted questions, and dates.

---

## Data Management

### Why JSON?

JSON (JavaScript Object Notation) is used for data management due to the following reasons:

- **Structured and Readable**: JSON offers a structured format that is easy to read and understand.
- **Language-Independent**: JSON is language-agnostic, making it versatile for potential future expansions in other programming languages.
- **Ease of Use in Python**: Python's built-in `json` module simplifies converting between JSON and Python data structures (e.g., dictionaries and lists).
- **Lightweight**: JSON is efficient for reading and writing data, ideal for small to medium-sized applications.
- **Human-Readable**: JSON is easy to inspect and modify, which is beneficial for debugging and version control.
  
While JSON is a great fit for this project, it may need to be replaced with a more scalable solution like a database for larger projects.

---

## Implementation Details

### admin_functions.py
Contains functions for managing quiz content:
- **add_category_or_question**: Adds new categories or questions to `qcm.json`.
- **delete_category**: Deletes categories or questions from `qcm.json`.

### user_functions.py
Handles user management tasks:
- **user_exists**: Checks if a user exists in `users.json`.
- **add_user**: Registers a new user.
- **login**: Authenticates users based on their username and password.

### main.py
The main entry point of the application:
- Manages user authentication and directs users to either the user or admin interface.

### quiz_app.py
Handles quiz functionality:
- Presents questions to users, records answers, and calculates scores.
- Updates `history.json` with the results of the quiz.

---

## Graphical Interface

The application features a simple and intuitive interface that facilitates easy interaction for both users and administrators. The design focuses on accessibility and ease of use, ensuring that users can navigate through quizzes, view past performance, and interact with admin functionalities with minimal complexity.

---

## Conclusion

The **Multiple-Choice Questionnaire (MCQ) Application** successfully implements a functional quiz system with both user and administrative functionalities. It serves as a solid foundation for educational quizzes, with potential for future enhancements such as improved security features and advanced functionalities.

---

## Github Repository

You can find the project repository here: [QCMpython on GitHub](https://github.com/raniabelak/QCMpython)

---

### Credits

The project was developed as part of the Advanced Programming course for 3rd-year Computer Science (Cybersecurity) students at USTHB.

---

