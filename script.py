import random
import unicodedata

def remove_accents(string):
    """Removes accents from a string."""
    return ''.join(
        char for char in unicodedata.normalize('NFD', string)
        if unicodedata.category(char) != 'Mn'
    )

def ask_word():
    # Random choice between asking for English or French first
    if random.choice([True, False]):
        english_word = input("Enter a word in English (or 'quit' to exit) : ")
        if english_word.lower() == "quit":
            return None, None
        french_word = input("Enter its translation in French : ")
    else:
        french_word = input("Enter a word in French (or 'quit' to exit) : ")
        if french_word.lower() == "quit":
            return None, None
        english_word = input("Enter its translation in English : ")
    
    return english_word, french_word

def save_word(english_word, french_word):
    with open("words.txt", "a") as file:
        file.write(f"{english_word}:{french_word}:0\n")  # Add 0 points by default

def load_words():
    words = []
    try:
        with open("words.txt", "r") as file:
            for line in file:
                english_word, french_word, points = line.strip().split(":")
                words.append((english_word, french_word, int(points)))
    except FileNotFoundError:
        print("No words have been recorded yet.")
    return words

def save_words(words):
    with open("words.txt", "w") as file:
        for english_word, french_word, points in words:
            file.write(f"{english_word}:{french_word}:{points}\n")

def display_words():
    words = load_words()
    if not words:
        print("No words have been recorded yet.")
        return
    
    print("\nList of recorded words :")
    for i, (english_word, french_word, points) in enumerate(words, start=1):
        print(f"{i}. {english_word} : {french_word} (Points : {points})")

def delete_word():
    words = load_words()
    if not words:
        print("No words have been recorded yet.")
        return
    
    display_words()
    try:
        choice = int(input("\nEnter the number of the word to delete : "))
        if 1 <= choice <= len(words):
            deleted_word = words.pop(choice - 1)
            save_words(words)
            print(f"The word '{deleted_word[0]} : {deleted_word[1]}' has been deleted.")
        else:
            print("Invalid number.")
    except ValueError:
        print("Please enter a valid number.")

def quiz():
    words = load_words()
    if not words:
        print("No words available for quizzing. Please add words first.")
        return
    
    # Filter tuples with 0 points or less than 7 points
    words_to_quiz = [(english_word, french_word, points) for english_word, french_word, points in words if points < 7]
    
    if not words_to_quiz:
        print("All words have reached the maximum number of points (7).")
        return
    
    # Choose a random word from those to quiz
    english_word, french_word, points = random.choice(words_to_quiz)
    
    # Randomly choose whether to ask for the translation in French or English
    if random.choice([True, False]):
        question = f"What is the translation in French of '{english_word}' ? "
        correct_answer = french_word
    else:
        question = f"What is the translation in English of '{french_word}' ? "
        correct_answer = english_word
    
    # Ask the question
    user_answer = input(question)
    
    # Ignore empty answers
    if not user_answer.strip():  # Check if the answer is empty or contains only spaces
        print("Empty answer ignored.")
        return
    
    # Normalize answers (remove accents and convert to lowercase)
    normalized_user_answer = remove_accents(user_answer.lower())
    normalized_correct_answer = remove_accents(correct_answer.lower())
    
    # Check the answer
    if normalized_user_answer == normalized_correct_answer:
        print("Correct !")
        points += 1  # Add 1 point
    else:
        print(f"Incorrect. The correct answer was : {correct_answer}")
    
    # Update the points in the word list
    for i, (ew, fw, p) in enumerate(words):
        if ew == english_word and fw == french_word:
            words[i] = (ew, fw, min(points, 7))  # Limit to 7 points maximum
            break
    
    # Save the updated words
    save_words(words)

def main():
    while True:
        print("\n1. Add a word")
        print("2. Quiz")
        print("3. Display the list of words")
        print("4. Delete a word")
        print("5. Quit")
        choice = input("Choose an option (1, 2, 3, 4 or 5) : ")
        
        if choice == "1":
            english_word, french_word = ask_word()
            if english_word is None or french_word is None:
                print("Thank you for using the program. Goodbye !")
                break
            save_word(english_word, french_word)
            print("Word saved successfully !")
        
        elif choice == "2":
            quiz()
        
        elif choice == "3":
            display_words()
        
        elif choice == "4":
            delete_word()
        
        elif choice == "5":
            print("Thank you for using the program. Goodbye !")
            break
        
        else:
            print("Invalid option. Please choose 1, 2, 3, 4 or 5.")

if __name__ == "__main__":
    main()
