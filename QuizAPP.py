import csv
import os
import time
from threading import Timer

class Question:
    def __init__(self, prompt, options, answer, difficulty="medium", time_limit=0):
        self.prompt = prompt
        self.options = options
        self.answer = answer
        self.difficulty = difficulty.lower()
        self.time_limit = time_limit  # in seconds (0 means no time limit)


def run_quiz(questions, player_name):
    score = 0
    time_up = False
    
    for question in questions:
        print("\n" + question.prompt)
        print(f"Difficulty: {question.difficulty.capitalize()}")
        
        for i, option in enumerate(question.options, 1):
            print(f"{i}. {option}")
        
        if question.time_limit > 0:
            print(f"\n You have {question.time_limit} seconds to answer!")
        
        user_answer = None
        
        def time_expired():
            nonlocal time_up
            time_up = True
            print("\nTime's up!")
        
        timer = None
        if question.time_limit > 0:
            timer = Timer(question.time_limit, time_expired)
            timer.start()
        
        start_time = time.time()
        
        while True:
            try:
                if time_up:
                    break
                
                user_input = input("Enter your answer (number): ").strip()
                if not user_input:
                    continue
                
                user_answer = int(user_input)
                if 1 <= user_answer <= len(question.options):
                    if timer:
                        timer.cancel()
                    break
                print(f"Please enter a number between 1 and {len(question.options)}")
            except ValueError:
                print("Please enter a valid number.")
        
        answer_time = time.time() - start_time
        
        if time_up:
            print(f" Time's up! The correct answer was: {question.answer}")
            time_up = False
        else:
            if question.time_limit > 0:
                print(f"Answered in {answer_time:.1f} seconds")
            
            if question.options[user_answer-1] == question.answer:
                print(" Correct!")
                
                # Score based on difficulty and speed
                if question.difficulty == "easy":
                    points = 1
                elif question.difficulty == "medium":
                    points = 2
                else:  # hard
                    points = 3
                
                # Bonus for answering quickly (if timed)
                if question.time_limit > 0 and answer_time < question.time_limit/2:
                    points += 1
                    print(" Speed bonus! +1 point")
                
                score += points
            else:
                print(f" Wrong! The correct answer was: {question.answer}")
    
    print(f"\n{player_name}, your total score is {score} points!")
    update_leaderboard(player_name, score)
    show_leaderboard()
    return score

def update_leaderboard(name, score):
    filename = "leaderboard.csv"
    data = []

    if os.path.exists(filename):
        with open(filename, "r") as file:
            reader = csv.reader(file)
            data = list(reader)
    
    data.append([name, str(score)])
    data.sort(key=lambda x: int(x[1]), reverse=True)
    data = data[:5]

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

def show_leaderboard():
    print("\n Top 5 Leaderboard:")
    filename = "leaderboard.csv"
    if not os.path.exists(filename):
        print("No leaderboard data yet.")
        return

    with open(filename, "r") as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader, 1):
            print(f"{i}. {row[0]} - {row[1]} points")

def select_difficulty():
    print("\nSelect difficulty level:")
    print("1. Easy (more time, simpler questions)")
    print("2. Medium (balanced)")
    print("3. Hard (less time, challenging questions)")
    
    while True:
        try:
            choice = int(input("Enter your choice (1-3): "))
            if 1 <= choice <= 3:
                return ["easy", "medium", "hard"][choice-1]
            print("Please enter a number between 1 and 3")
        except ValueError:
            print("Please enter a valid number.")

def get_questions(difficulty):
    # Base questions
    all_questions = [
        Question("What is the capital of France?", 
                ["London", "Berlin", "Paris", "Madrid"], 
                "Paris", "easy", 15),
        
        Question("Which language is this quiz written in?", 
                ["Java", "C++", "Python", "JavaScript"], 
                "Python", "easy", 10),
        
        Question("What is 2 + 2?", 
                ["3", "4", "5", "6"], 
                "4", "easy", 8),
        
        Question("Which of these is not a Python data structure?", 
                ["List", "Tuple", "Array", "Dictionary"], 
                "Array", "medium", 12),
        
        Question("What year was Python created?", 
                ["1989", "1995", "2000", "2005"], 
                "1989", "medium", 10),
        
        Question("What does the 'self' keyword refer to in Python?", 
                ["The module", "The class instance", "The parent class", "The return value"], 
                "The class instance", "hard", 15),
        
        Question("Which Python framework is used for web development?", 
                ["Django", "Pandas", "NumPy", "Matplotlib"], 
                "Django", "medium", 12),
        
        Question("What is the time complexity of a Python dictionary lookup?", 
                ["O(1)", "O(n)", "O(log n)", "O(n²)"], 
                "O(1)", "hard", 15),
        
        Question("Which Python keyword is used to define a function?", 
                ["func", "def", "function", "define"], 
                "def", "easy", 8),
        
        Question("What does PEP stand for in Python?", 
                ["Python Enhancement Proposal", "Python Execution Process", 
                 "Programmer's Enhancement Protocol", "Python Error Prevention"], 
                "Python Enhancement Proposal", "hard", 20)
    ]
    
    # Filter questions by difficulty
    filtered = [q for q in all_questions if q.difficulty == difficulty]
    
    # Adjust time limits based on difficulty
    for q in filtered:
        if difficulty == "easy":
            q.time_limit = int(q.time_limit * 1.5)
        elif difficulty == "hard":
            q.time_limit = int(q.time_limit * 0.7)
    
    # If not enough questions for the selected difficulty, add some from other levels
    if len(filtered) < 5:
        needed = 5 - len(filtered)
        others = [q for q in all_questions if q.difficulty != difficulty]
        filtered.extend(others[:needed])
    
    return filtered

def main():
    print(" Welcome to the Python Quiz App!")
    name = input("Enter your name: ")
    
    while True:
        difficulty = select_difficulty()
        questions = get_questions(difficulty)
        
        print(f"\nHello, {name}! Get ready for {difficulty} questions.")
        print("Answer by entering the number of your choice.")
        
        run_quiz(questions, name)
        
        play_again = input("\nWould you like to play again? (yes/no): ").lower()
        if play_again != "yes":
            print("👋 Thanks for playing! Goodbye.")
            break

if __name__ == "__main__":
    main()