import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random

# Create a connection to database (it will create the file if it doesn't exist)
conn = sqlite3.connect('quiz.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS quiz_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    category TEXT NOT NULL
)
''')

# Sample questions and answers
quiz_data = [
    ("What is the capital of France?", "Paris", "Geography"),
    ("Who painted the Mona Lisa?", "Leonardo da Vinci", "Art"),
    ("What is the chemical symbol for gold?", "Au", "Science"),
    ("What planet is known as the Red Planet?", "Mars", "Science"),
    ("Who wrote 'Romeo and Juliet'?", "William Shakespeare", "Literature"),
    ("What is the largest ocean on Earth?", "Pacific Ocean", "Geography"),
    ("What is the square root of 144?", "12", "Mathematics"),
    ("Who was the first president of the United States?", "George Washington", "History"),
    ("What is the hardest natural substance on Earth?", "Diamond", "Science"),
    ("What country is known as the Land of the Rising Sun?", "Japan", "Geography"),
    ("Who developed the theory of relativity?", "Albert Einstein", "Science"),
    ("What is the longest river in the world?", "Nile River", "Geography"),
    ("What year did World War II end?", "1945", "History"),
    ("What element has the atomic number 1?", "Hydrogen", "Science"),
    ("Who composed the 'Moonlight Sonata'?", "Ludwig van Beethoven", "Music"),
    ("What is the capital of Japan?", "Tokyo", "Geography"),
    ("Who painted 'The Starry Night'?", "Vincent van Gogh", "Art"),
    ("What is the speed of light?", "299,792,458 meters per second", "Science"),
    ("What is the largest planet in our solar system?", "Jupiter", "Science"),
    ("Who wrote '1984'?", "George Orwell", "Literature")
]

# Insert data into the table
cursor.executemany('INSERT INTO quiz_questions (question, answer, category) VALUES (?, ?, ?)', quiz_data)

# Commit the changes
conn.commit()

# Function to retrieve all questions and answers
def get_all_questions():
    cursor.execute('SELECT * FROM quiz_questions')
    return cursor.fetchall()

# Function to get questions by category
def get_questions_by_category(category):
    cursor.execute('SELECT * FROM quiz_questions WHERE category = ?', (category,))
    return cursor.fetchall()

# Example usage:
print("All questions:")
all_questions = get_all_questions()
for question in all_questions:
    print(f"\nID: {question[0]}")
    print(f"Question: {question[1]}")
    print(f"Answer: {question[2]}")
    print(f"Category: {question[3]}")

print("\nScience questions:")
science_questions = get_questions_by_category('Science')
for question in science_questions:
    print(f"\nID: {question[0]}")
    print(f"Question: {question[1]}")
    print(f"Answer: {question[2]}")

# Close the connection
conn.close()



class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')

        # Database connection
        self.conn = sqlite3.connect('quiz.db')
        self.cursor = self.conn.cursor()

        # Variables
        self.current_question = None
        self.score = 0
        self.total_questions = 0
        self.categories = self.get_categories()
        self.selected_category = tk.StringVar()

        self.setup_gui()
        self.load_question()

    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Category selection
        ttk.Label(main_frame, text="Select Category:").grid(row=0, column=0, pady=10)
        category_combo = ttk.Combobox(main_frame, textvariable=self.selected_category, values=["All"] + self.categories)
        category_combo.grid(row=0, column=1, pady=10)
        category_combo.set("All")
        category_combo.bind("<<ComboboxSelected>>", lambda e: self.load_question())

        # Score display
        self.score_label = ttk.Label(main_frame, text="Score: 0/0")
        self.score_label.grid(row=0, column=2, pady=10)

        # Question display
        self.question_frame = ttk.Frame(main_frame, padding="10")
        self.question_frame.grid(row=1, column=0, columnspan=3, pady=20)
        
        self.question_label = ttk.Label(self.question_frame, text="", wraplength=600)
        self.question_label.grid(row=0, column=0, pady=10)

        # Answer entry
        self.answer_var = tk.StringVar()
        self.answer_entry = ttk.Entry(main_frame, textvariable=self.answer_var, width=50)
        self.answer_entry.grid(row=2, column=0, columnspan=3, pady=10)

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=20)

        ttk.Button(button_frame, text="Submit Answer", command=self.check_answer).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Next Question", command=self.load_question).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Show Answer", command=self.show_answer).grid(row=0, column=2, padx=5)

        # Bind Enter key to submit answer
        self.root.bind('<Return>', lambda e: self.check_answer())

    def get_categories(self):
        self.cursor.execute('SELECT DISTINCT category FROM quiz_questions')
        return [category[0] for category in self.cursor.fetchall()]

    def load_question(self):
        category = self.selected_category.get()
        if category == "All":
            self.cursor.execute('SELECT * FROM quiz_questions')
        else:
            self.cursor.execute('SELECT * FROM quiz_questions WHERE category = ?', (category,))
        
        questions = self.cursor.fetchall()
        if questions:
            self.current_question = random.choice(questions)
            self.question_label.config(text=f"Category: {self.current_question[3]}\n\nQuestion: {self.current_question[1]}")
            self.answer_var.set("")  # Clear previous answer
            self.answer_entry.focus()  # Focus on answer entry
        else:
            messagebox.showinfo("Info", "No questions available for this category!")

    def check_answer(self):
        if not self.current_question:
            return

        user_answer = self.answer_var.get().strip().lower()
        correct_answer = self.current_question[2].lower()

        self.total_questions += 1
        if user_answer == correct_answer:
            self.score += 1
            messagebox.showinfo("Correct!", "Your answer is correct!")
        else:
            messagebox.showinfo("Incorrect!", f"Sorry, the correct answer is: {self.current_question[2]}")

        self.score_label.config(text=f"Score: {self.score}/{self.total_questions}")
        self.load_question()

    def show_answer(self):
        if self.current_question:
            messagebox.showinfo("Answer", f"The answer is: {self.current_question[2]}")

    def __del__(self):
        # Close database connection when the application closes
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()