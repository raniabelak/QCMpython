import json

def add_category_or_question(file_path):

    # Charger ou initialiser le fichier
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"categories": []}
    
    # Obtenir le nom de la catégorie
    category_name = input("Enter the category name: ").strip()
    
    # Vérifier si la catégorie existe
    
    category = next((cat for cat in data["categories"] if cat["name"].lower() == category_name.lower()), None)
    
    if not category:
        # Créer une nouvelle catégorie si elle n'existe pas
        category_id = len(data["categories"]) + 1
        category = {
            "id": category_id,
            "name": category_name,
            "questions": []
        }
        data["categories"].append(category)
        print(f"Created new category '{category_name}'.")
    else:
        print(f"Adding to existing category '{category_name}'.")
    
    while True:
        # Ajouter une question
        question_text = input("Enter your question: ")
        options = []
        
        print("Enter the four options:")
        for letter in ["a", "b", "c", "d"]:
            option_text = input(f"Option {letter}: ")
            options.append({"id": letter, "text": option_text})
        
        correct_answer = input("Enter the correct answer (a, b, c, or d): ").strip().lower()
        
        question_id = len(category["questions"]) + 1
        new_question = {
            "id": question_id,
            "question": question_text,
            "options": options,
            "correct_answer": correct_answer
        }
        category["questions"].append(new_question)
        
        # Demander à l'utilisateur s'il veut ajouter une autre question
        add_more = input("Do you want to add another question? (yes/no): ").strip().lower()
        if add_more != "yes":
            break
    
    # Sauvegarder le fichier
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    print(f"Category '{category_name}' and its questions have been saved to the file.")

add_category_or_question('questions.json')