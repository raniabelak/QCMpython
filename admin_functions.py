import json
import os
import sys

# Dynamically resolves the base path for file operations
def get_base_path():
    if getattr(sys, 'frozen', False):  # Check if the script is running as an executable
        return sys._MEIPASS  # use pyinstaller temp directory
    else:
        return os.path.dirname(os.path.abspath(__file__))  # use script directory

# Resolves the full path for a file based on the base path
def get_file_path(filename):
    return os.path.join(get_base_path(), filename)

def add_category_or_question(file_name):

    file_path = get_file_path(file_name)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"categories": []}
    except json.JSONDecodeError:
        print("Error: The file is corrupted or not in JSON format.")
        return
    
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
        
        add_more = input("Do you want to add another question? (yes/no): ").strip().lower()
        if add_more != "yes":
            break

    # Save the updated data to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    
    print(f"Category '{category_name}' and its questions have been saved successfully!")


def delete_category(file_name):
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
    