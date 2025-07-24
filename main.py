import csv

def load_flashcards_from_csv(filename):
    cards = []
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cards.append({
                    "question": row["question"],
                    "answer": row["answer"]
                })
    except FileNotFoundError:
        print("❌ Файл не знайдено.")
    return cards

# 🔽 Початок гри
print("🎓 Вітаємо у Flashcard грі!")

subject = input("📝 Введіть тему (наприклад: math): ").strip().lower()
filename = f"subjects/{subject}.csv"

cards = load_flashcards_from_csv(filename)

if not cards:
    print("😢 Немає доступних карток для цієї теми.")
else:
    print(f"\n📚 Тема: {subject.capitalize()} — Починаємо гру!\n")
    score = 0

    for card in cards:
        user_answer = input(f"❓ {card['question']} \n👉 Ваша відповідь: ").strip()
        correct_answer = card['answer'].strip()

        if user_answer.lower() == correct_answer.lower():
            print("✅ Правильно!\n")
            score += 1
        else:
            print(f"❌ Неправильно. Правильна відповідь: {correct_answer}\n")

    print(f"🎯 Ваш результат: {score} з {len(cards)}")
