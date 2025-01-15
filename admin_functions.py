import json
import os
import sys

def get_base_path():
    """
    Dynamically resolves the base path for file operations.
    - If running as an executable, returns the temporary directory created by PyInstaller.
    - If running as a script, returns the directory of the script.
    """
    if getattr(sys, 'frozen', False):  # Check if the script is running as an executable
        return sys._MEIPASS  # Use the temporary directory created by PyInstaller
    else:
        return os.path.dirname(os.path.abspath(__file__))  # Use the script's directory

def get_file_path(filename):
    """
    Resolves the full path for a file based on the base path.
    """
    return os.path.join(get_base_path(), filename)

def add_category_or_question(file_name):
    """
    Adds a new category or question to the quiz data.
    """
    file_path = get_file_path(file_name)  # Resolve the file path
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"categories": []}
    except json.JSONDecodeError:
        print("Error: The file is corrupted or not in JSON format.")
        return
    
    # Ask for the category name
    category_name = input("Enter the category name: ").strip()
    
    # Check if the category exists
    category = None
    for cat in data["categories"]:
        if cat["name"].lower() == category_name.lower():
            category = cat
            break
    
    if not category:
        # Create a new category if it doesn't exist
        new_category_id = 1 if not data["categories"] else data["categories"][-1]["id"] + 1
        new_category = {
            "id": new_category_id,
            "name": category_name,
            "questions": []
        }
        data["categories"].append(new_category)
        category = new_category
        print(f"Created new category '{category_name}' with ID {new_category_id}.")
        
        # Save the updated file immediately
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
    else:
        print(f"Adding to existing category '{category_name}'.")
    
    # Ask if the user wants to add questions
    add_question = input("Do you want to add a question to this category? (yes/no): ").strip().lower()
    if add_question != "yes":
        print("Category added successfully!")
        return
    
    # Loop to add questions
    while True:
        question_text = input("Enter the question: ").strip()
        options = []
        
        # Get options
        for option_id in ["a", "b", "c", "d"]:
            option_text = input(f"Enter option {option_id}: ").strip()
            options.append({"id": option_id, "text": option_text})
        
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
        
        # Ask if the user wants to add another question
        add_more = input("Do you want to add another question? (yes/no): ").strip().lower()
        if add_more != "yes":
            break

    # Save the updated data to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    
    print(f"Category '{category_name}' and its questions have been saved successfully!")

def delete_category(file_name):
    """
    Deletes a category from the quiz data.
    """
    file_path = get_file_path(file_name)  # Resolve the file path
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("File not found.")
        return
    except json.JSONDecodeError:
        print("Error: The file is corrupted or not in JSON format.")
        return

    # Show categories 
    print("Categories:")
    for category in data["categories"]:
        print(f"{category['id']}. {category['name']}")

    # Ask for category ID to delete
    category_id = int(input("Enter the category ID to delete: "))
    category = next((cat for cat in data["categories"] if cat["id"] == category_id), None)

    if category:
        # Delete the category
        data["categories"].remove(category)
        print(f"Category '{category['name']}' has been deleted.")
    else:
        print("Category not found.")
    
    # Save the file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    
def delete_question(file_name):
    """
    Deletes a question from a category in the quiz data.
    """
    file_path = get_file_path(file_name)  # Resolve the file path
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("File not found.")
        return
    except json.JSONDecodeError:
        print("Error: The file is corrupted or not in JSON format.")
        return

    print("Categories:")
    for category in data["categories"]:
        print(f"{category['id']}. {category['name']}")
        
    category_id = int(input("Enter the category ID: "))
    category = next((cat for cat in data["categories"] if cat["id"] == category_id), None)
  
    if category:
        print("Questions:")
        for question in category["questions"]:
            print(f"{question['id']}. {question['question']}")
        
        question_id = int(input("Enter the question ID to delete: "))
        question = next((q for q in category["questions"] if q["id"] == question_id), None)
        
        if question:
            category["questions"].remove(question)
            print("Question deleted successfully.")
        else:
            print("Question not found.")

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
    else:
        print("Category not found.")

# Example usage
if __name__ == "__main__":
    file_name = "qcm.json"  # Replace with your JSON file name
    add_category_or_question(file_name)
    # delete_category(file_name)
    # delete_question(file_name)