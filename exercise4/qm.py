import time
import json
import os

# ---------------- Sample Questions ---------------- #
questions = {
    "Science": {
        "easy": [
            {"question": "What planet is known as the Red Planet?",
             "options": ["Earth", "Mars", "Jupiter", "Venus"], "answer": 1},
            {"question": "What gas do plants absorb from the air?",
             "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"], "answer": 2},
            {"question": "How many legs does an insect have?",
             "options": ["4", "6", "8", "10"], "answer": 1},
            {"question": "What is H2O commonly known as?",
             "options": ["Salt", "Oxygen", "Water", "Helium"], "answer": 2},
            {"question": "What part of the plant conducts photosynthesis?",
             "options": ["Roots", "Stem", "Leaves", "Flower"], "answer": 2}
        ],
        "hard": [
            {"question": "What is the atomic number of Carbon?",
             "options": ["4", "6", "8", "12"], "answer": 1},
            {"question": "What is the speed of light in vacuum?",
             "options": ["300,000 km/s", "150,000 km/s", "299,792 km/s", "100,000 km/s"], "answer": 2},
            {"question": "What is Newton's 2nd law?",
             "options": ["F=ma", "E=mc^2", "V=IR", "a^2 + b^2 = c^2"], "answer": 0},
            {"question": "Which element has the chemical symbol 'Fe'?",
             "options": ["Iron", "Fluorine", "Fermium", "Francium"], "answer": 0},
            {"question": "What part of the brain regulates balance?",
             "options": ["Cerebrum", "Cerebellum", "Brainstem", "Hippocampus"], "answer": 1}
        ]
    },
    "History": {
        "easy": [
            {"question": "Who was the first President of the United States?",
             "options": ["Abraham Lincoln", "George Washington", "John Adams", "Thomas Jefferson"], "answer": 1},
            {"question": "In what year did World War II end?",
             "options": ["1945", "1939", "1918", "1950"], "answer": 0},
            {"question": "What ancient civilization built the pyramids?",
             "options": ["Romans", "Greeks", "Egyptians", "Mayans"], "answer": 2},
            {"question": "Who discovered America?",
             "options": ["Christopher Columbus", "Marco Polo", "Vasco da Gama", "Ferdinand Magellan"], "answer": 0},
            {"question": "Which country gifted the Statue of Liberty to the US?",
             "options": ["France", "Spain", "Italy", "Germany"], "answer": 0}
        ],
        "hard": [
            {"question": "Who was the British PM during WWII?",
             "options": ["Winston Churchill", "Neville Chamberlain", "Clement Attlee", "Harold Wilson"], "answer": 0},
            {"question": "What event started WWI?",
             "options": ["Treaty of Versailles", "Assassination of Archduke Franz Ferdinand", "Pearl Harbor", "D-Day"], "answer": 1},
            {"question": "Where was Napoleon born?",
             "options": ["Paris", "Corsica", "Rome", "London"], "answer": 1},
            {"question": "What empire ruled India before British colonization?",
             "options": ["Maurya", "Mughal", "Gupta", "Ottoman"], "answer": 1},
            {"question": "When was the UN founded?",
             "options": ["1940", "1945", "1939", "1950"], "answer": 1}
        ]
    },
    "Sports": {
        "easy": [
            {"question": "How many players are there in a soccer team?",
             "options": ["9", "10", "11", "12"], "answer": 2},
            {"question": "Which sport uses a bat and ball?",
             "options": ["Soccer", "Tennis", "Basketball", "Baseball"], "answer": 3},
            {"question": "How long is a marathon?",
             "options": ["5 km", "26.2 miles", "13.1 miles", "42 km"], "answer": 1},
            {"question": "Where did the Olympics originate?",
             "options": ["Greece", "USA", "Rome", "China"], "answer": 0},
            {"question": "What color flag means stop in racing?",
             "options": ["Green", "Yellow", "Red", "Blue"], "answer": 2}
        ],
        "hard": [
            {"question": "Which country has the most FIFA World Cups?",
             "options": ["Italy", "Brazil", "Germany", "Argentina"], "answer": 1},
            {"question": "Who holds the 100m world record?",
             "options": ["Tyson Gay", "Yohan Blake", "Usain Bolt", "Carl Lewis"], "answer": 2},
            {"question": "How many NBA titles does Michael Jordan have?",
             "options": ["5", "6", "7", "8"], "answer": 1},
            {"question": "In which sport is the Davis Cup awarded?",
             "options": ["Golf", "Tennis", "Cricket", "Baseball"], "answer": 1},
            {"question": "What year were the first modern Olympics held?",
             "options": ["1896", "1900", "1920", "1888"], "answer": 0}
        ]
    }
}

# ---------------- High Score Storage ---------------- #
def load_high_scores():
    if os.path.exists("highscores.json"):
        with open("highscores.json", "r") as file:
            return json.load(file)
    return {}

def save_high_scores(scores):
    with open("highscores.json", "w") as file:
        json.dump(scores, file, indent=2)

# ---------------- Quiz Functions ---------------- #
def print_progress(current, total):
    bar_len = 20
    filled = int(bar_len * current / total)
    bar = "█" * filled + "░" * (bar_len - filled)
    percent = int(100 * current / total)
    print(f"[{bar}] {percent}% Complete")

def ask_questions(q_list):
    score = 0
    wrong_answers = []
    total = len(q_list)
    for i, q in enumerate(q_list, start=1):
        print(f"\nQuestion {i}/{total}: {q['question']}")
        print_progress(i - 1, total)

        for idx, opt in enumerate(q['options']):
            print(f"{chr(65+idx)}) {opt}")
        
        start = time.time()
        answer = input("Your answer (A/B/C/D): ").strip().upper()
        end = time.time()
        time_taken = round(end - start, 2)

        try:
            answer_index = ord(answer) - 65
            if answer_index == q['answer']:
                print(f"✅ Correct! (+10 points)\nTime: {time_taken} seconds")
                score += 10
            else:
                correct = q['options'][q['answer']]
                print(f"❌ Incorrect. Correct answer: {correct}\nTime: {time_taken} seconds")
                wrong_answers.append((q['question'], q['options'], q['answer'], answer))
        except:
            print("❌ Invalid input. Skipped.")
            wrong_answers.append((q['question'], q['options'], q['answer'], answer))
    return score, wrong_answers

# ---------------- Main Program ---------------- #
def main():
    highscores = load_high_scores()
    print("=== QUIZ MASTER ===")
    categories = list(questions.keys())
    print("Categories:", ", ".join(categories))

    category = input("Choose category: ").capitalize()
    if category not in questions:
        print("Invalid category.")
        return

    difficulty = input("Choose difficulty (easy/hard): ").lower()
    if difficulty not in ["easy", "hard"]:
        print("Invalid difficulty.")
        return

    quiz_list = questions[category][difficulty]
    print(f"\nSelected: {category} ({difficulty.capitalize()})")

    score, wrongs = ask_questions(quiz_list)

    print(f"\nFINAL SCORE: {score}/{len(quiz_list) * 10} ({score//10}/{len(quiz_list)} correct)")

    # Check for new high score
    key = f"{category}_{difficulty}"
    prev_best = highscores.get(key, 0)
    if score > prev_best:
        highscores[key] = score
        save_high_scores(highscores)
        print(f"🎉 New personal best in {category} ({difficulty.capitalize()})!")
    else:
        print(f"🏁 Your best in {category} ({difficulty.capitalize()}): {prev_best}")

    # Show wrong answers
    if wrongs:
        print("\n📘 Review Your Mistakes:")
        for q, opts, ans_idx, user_ans in wrongs:
            correct = opts[ans_idx]
            print(f"❌ {q}")
            print(f"   Your answer: {user_ans}")
            print(f"   Correct answer: {correct}")

if __name__ == "__main__":
    main()
