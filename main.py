import csv
import os
import random

def load_questions(subject):
    filename = os.path.join("subjects", f"{subject}.csv")

    full_path = os.path.abspath(filename)
    print("🔍 Перевірка шляху:", full_path)
    
    if not os.path.exists(filename):
        print("❌ Файл не знайдено.")
        return []
    
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def quiz_mode(questions):
    correct = 0
    total = len(questions)
    wrong = 0
    random.shuffle(questions)

    wrong_questions = []
    for q in questions:
        print("\n❓", q['question'])
        print(f"  A. {q['A']}")
        print(f"  B. {q['B']}")
        print(f"  C. {q['C']}")
        print(f"  D. {q['D']}")
        answer = input("👉 Ваша відповідь (A/B/C/D), \nЯкщо хочете вийти напишіть q: ").strip().upper()
        if answer == q['correct'].strip().upper():
            print("✅ Правильно!")
            correct += 1
        elif answer == "Q":
            break
        else:
            wrong += 1
            print(f"❌ Неправильно. Правильна відповідь: {q['correct'].upper()}")
            wrong_questions.append(q)
    output = show_statistics(correct, wrong)   
    while output == "retry":
        correct = 0
        total = len(questions)
        wrong = 0
        random.shuffle(questions)
        for q in wrong_questions:
            print("\n❓", q['question'])
            print(f"  A. {q['A']}")
            print(f"  B. {q['B']}")
            print(f"  C. {q['C']}")
            print(f"  D. {q['D']}")
            answer = input("👉 Ваша відповідь (A/B/C/D), \nЯкщо хочете вийти напишіть q: ").strip().upper()
        if answer == q['correct'].strip().upper():
            print("✅ Правильно!")
            correct += 1
        elif answer == "Q":
            break
        else:
            wrong += 1
            print(f"❌ Неправильно. Правильна відповідь: {q['correct'].upper()}")
            wrong_questions.append(q)
        output = show_statistics(correct, wrong)


        

def main():
    print("🎉 Вітаємо у грі-квізі! 🎉")
    print("Ви отримаєте запитання з 4 варіантами відповідей. Оберіть правильну букву.")
    print("Готові? Починаємо!\n")
    choice = input("Якщо хочете вибрати з створених тестів, напишіть A, якщо створити свій напишіть B ")
    if choice == "B" or choice == "В":
        card, topic = add_card()
        write_card(card, topic)
    subject = input("🔍 Введіть назву предмета (наприклад, math): ").strip()
    filename = os.path.join("subjects", f"{subject}.csv")
    if not os.path.exists(filename):
        print("Такої теми не існує, створіть її самі")
        card, topic = add_card
        write_card(card, topic)
    questions = load_questions(subject)
    if questions:
        quiz_mode(questions)
    else:
        print("😕 Упс! Не вдалося завантажити запитання.")
    print("\n👋 Дякуємо за гру!")

def add_card():
    topic = input("Введіть тему запитання ")
    question = input("Введіть питання: ")
    answer = input("Введіть правильну відповідь: ")
    wrong_answer1 = input("Введіть неправильну відповідь 1: ")
    wrong_answer2 = input("Введіть неправильну відповідь 2: ")
    wrong_answer3 = input("Введіть неправильну відповідь 3: ")
    card = {"question": question, "answer": answer, "wrong_answers": [wrong_answer1, wrong_answer2, wrong_answer3]} 
    print(f"\nКартку додано: '{question}' | Правильна: '{answer}'")
    return card, topic

def write_card(card, topic):
    folder = "subjects"
    filename = os.path.join(folder, f"{topic}.csv")
    file_exists = os.path.exists(filename)
    with open(filename, "a", newline = "", encoding = "utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["question", "A", "B", "C", "D", "correct"])

        answers = card["wrong_answers"].copy()
        answers.append(card["answer"])
        random.shuffle(answers)

        answers_dict = {}
        answer_keys = ["A", "B", "C", "D"]
        for i in range(4):
            answers_dict[answer_keys[i]] = answers[i]
            if answers[i] == card["answer"]:
                right_answer_letter = answer_keys[i]

        writer.writerow([
            card["question"],
            answers_dict["A"],
            answers_dict["B"],
            answers_dict["C"],
            answers_dict["D"],
            right_answer_letter
        ])
    
    
    

def show_statistics(correct_answers, wrong_answers):
    """
    Displays quiz statistics including:
    - Number of correct and wrong answers
    - Percentage score

    Then asks the user what to do next:
    - Option 1: Practice wrong answers again (returns "retry")
    - Option 2: Exit the quiz (returns "exit")

    Parameters:
    - correct_answers (list): List of correctly answered question identifiers
    - wrong_answers (list): List of wrongly answered question identifiers

    Returns:
    - str: "retry" if the user wants to practice wrong answers again
           "exit" if the user wants to finish
    """
    total = correct_answers + wrong_answers
    if total == 0:
        print("⚠️ Жодного запитання не було пройдено.")
        return "exit"

    correct_count = correct_answers
    wrong_count = wrong_answers
    score_percent = round((correct_count / total) * 100, 2)

    print("\n📊 --- Статистика тесту ---")
    print(f"✅ Правильних відповідей: {correct_count}")
    print(f"❌ Неправильних відповідей: {wrong_count}")
    print(f"🎯 Результат: {score_percent}%")

    if wrong_count > 0:
        print("\nЩо хочеш зробити далі?")
        print("1. 🔁 Повторити помилки")
        print("2. 🚪 Вийти з тесту")

        choice = input("Введи 1 або 2: ").strip()
        if choice == "1":
            return "retry"
        else:
            return "exit"
    else:
        print("\n🎉 Ідеально! Всі відповіді правильні!")
        return "exit"

if __name__ == "__main__":
    main()

