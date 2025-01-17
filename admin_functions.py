import json

def load_json_file(file_path):
    """Load JSON data from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if not data:  # Check if the file is empty
                print("The file is empty.")
                return {"categories": []}
            return data
    except FileNotFoundError:
        print("File not found. A new file will be created.")
        return {"categories": []}  # Return an empty structure if the file doesn't exist
    except json.JSONDecodeError:
        print("The file contains invalid JSON. A new structure will be created.")
        return {"categories": []}  # Return an empty structure if JSON is invalid

def save_json_file(file_path, data):
    """Save data to a JSON file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def add_category(file_path):
    """Add a new category to the quiz."""
    data = load_json_file(file_path)

    # Ask for the category name
    while True:
        category_name = input("Enter the category name: ").strip()
        if category_name:
            break
        print("Error: Category name cannot be empty.")

    # Check if the category already exists
    category = next((cat for cat in data["categories"] if cat["name"].lower() == category_name.lower()), None)

    if category:
        print(f"Category '{category_name}' already exists.")
        return

    # Create a new category
    new_category_id = 1 if not data["categories"] else data["categories"][-1]["id"] + 1
    new_category = {
        "id": new_category_id,
        "name": category_name,
        "questions": []
    }
    data["categories"].append(new_category)
    save_json_file(file_path, data)
    print(f"Category '{category_name}' with ID {new_category_id} has been added successfully!")

def add_question(file_path):
    """Add a new question to an existing category."""
    data = load_json_file(file_path)

    # Show existing categories
    print("Existing Categories:")
    for category in data["categories"]:
        print(f"{category['id']}. {category['name']}")

    # Ask for category ID
    while True:
        try:
            category_id = int(input("Enter the category ID to add a question: "))
            break
        except ValueError:
            print("Error: Invalid input. Please enter a valid number.")

    # Find the selected category
    category = next((cat for cat in data["categories"] if cat["id"] == category_id), None)
    if not category:
        print("Category not found.")
        return

    # Loop to add questions
    while True:
        question_text = input("Enter the question: ").strip()
        if not question_text:
            print("Error: Question cannot be empty.")
            continue

        options = []
        for option_id in ["a", "b", "c", "d"]:
            while True:
                option_text = input(f"Enter option {option_id}: ").strip()
                if option_text:
                    options.append({"id": option_id, "text": option_text})
                    break
                print("Error: Option cannot be empty.")

        while True:
            correct_answer = input("Enter the correct answer (a, b, c, or d): ").strip().lower()
            if correct_answer in ["a", "b", "c", "d"]:
                break
            print("Invalid input. Please enter one of: a, b, c, or d.")

        # Add the question to the category
        question_id = len(category["questions"]) + 1
        category["questions"].append({
            "id": question_id,
            "question": question_text,
            "options": options,
            "correct_answer": correct_answer
        })

        while True:
            add_more = input("Do you want to add another question? (yes/no): ").strip().lower()
            if add_more in ["yes", "no"]:
                break
            print("Invalid input. Please enter 'yes' or 'no'.")

        if add_more == "no":
            break

    # Save the updated data to the file
    save_json_file(file_path, data)
    print(f"Questions have been added to category '{category['name']}' successfully!")

def delete_category(file_path):
    """Delete a category from the quiz."""
    data = load_json_file(file_path)

    # Show categories
    print("Categories:")
    for category in data["categories"]:
        print(f"{category['id']}. {category['name']}")

    # Ask for category ID to delete
    while True:
        try:
            category_id = int(input("Enter the category ID to delete: "))
            break
        except ValueError:
            print("Error: Invalid input. Please enter a valid number.")

    category = next((cat for cat in data["categories"] if cat["id"] == category_id), None)
    if category:
        data["categories"].remove(category)
        print(f"Category '{category['name']}' has been deleted.")
        save_json_file(file_path, data)
    else:
        print("Category not found.")

def delete_question(file_path):
    """Delete a question from a category."""
    data = load_json_file(file_path)

    # Show categories
    print("Categories:")
    for category in data["categories"]:
        print(f"{category['id']}. {category['name']}")

    # Ask for category ID
    while True:
        try:
            category_id = int(input("Enter the category ID: "))
            break
        except ValueError:
            print("Error: Invalid input. Please enter a valid number.")

    category = next((cat for cat in data["categories"] if cat["id"] == category_id), None)
    if not category:
        print("Category not found.")
        return

    # Show questions in the selected category
    print("Questions:")
    for question in category["questions"]:
        print(f"{question['id']}. {question['question']}")

    # Ask for question ID to delete
    while True:
        try:
            question_id = int(input("Enter the question ID to delete: "))
            break
        except ValueError:
            print("Error: Invalid input. Please enter a valid number.")

    question = next((q for q in category["questions"] if q["id"] == question_id), None)
    if question:
        category["questions"].remove(question)
        print("Question deleted successfully.")
        save_json_file(file_path, data)
    else:
        print("Question not found.")
