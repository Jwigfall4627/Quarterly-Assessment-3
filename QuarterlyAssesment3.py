import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from random import shuffle

class QuizApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("800x600")
        
        # Database connection
        self.conn = sqlite3.connect('questions.db')
        self.cursor = self.conn.cursor()
        
        # Variables
        self.current_question = 0
        self.score = 0
        self.questions = []
        self.selected_table = tk.StringVar()
        
        # Initialize UI
        self.setup_ui()
        
    def setup_ui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Table selection
        ttk.Label(main_frame, text="Select Course:").grid(row=0, column=0, pady=10)
        table_combo = ttk.Combobox(main_frame, textvariable=self.selected_table)
        table_combo['values'] = ('DS3850', 'DS3860')
        table_combo.grid(row=0, column=1, pady=10)
        table_combo.set('DS3850')  # Default value
        
        # Start button
        ttk.Button(main_frame, text="Start Quiz", command=self.start_quiz).grid(row=1, column=0, columnspan=2, pady=10)
        
        # Question frame
        self.question_frame = ttk.Frame(main_frame)
        self.question_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Question label
        self.question_label = ttk.Label(self.question_frame, text="", wraplength=600)
        self.question_label.grid(row=0, column=0, pady=10)
        
        # Answer entry
        self.answer_entry = ttk.Entry(self.question_frame, width=50)
        self.answer_entry.grid(row=1, column=0, pady=10)
        
        # Submit button
        self.submit_btn = ttk.Button(self.question_frame, text="Submit Answer", command=self.check_answer)
        self.submit_btn.grid(row=2, column=0, pady=10)
        
        # Score label
        self.score_label = ttk.Label(self.question_frame, text="Score: 0/0")
        self.score_label.grid(row=3, column=0, pady=10)
        
        # Initially hide the question frame
        self.question_frame.grid_remove()
        
    def start_quiz(self):
        # Get questions from selected table
        table = self.selected_table.get()
        try:
            self.cursor.execute(f"SELECT * FROM {table}")
            self.questions = self.cursor.fetchall()
            shuffle(self.questions)  # Randomize question order
            
            self.current_question = 0
            self.score = 0
            self.question_frame.grid()
            self.show_question()
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
    
    def show_question(self):
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question][1]  # Assuming question is in second column
            self.question_label.config(text=f"Question {self.current_question + 1}: {question}")
            self.answer_entry.delete(0, tk.END)
            self.score_label.config(text=f"Score: {self.score}/{self.current_question}")
        else:
            self.show_final_score()
    
    def check_answer(self):
        if self.current_question < len(self.questions):
            user_answer = self.answer_entry.get().strip().lower()
            correct_answer = str(self.questions[self.current_question][2]).strip().lower()  # Assuming answer is in third column
            
            if user_answer == correct_answer:
                self.score += 1
                messagebox.showinfo("Correct!", "Your answer is correct!")
            else:
                messagebox.showinfo("Incorrect", f"The correct answer was: {correct_answer}")
            
            self.current_question += 1
            self.show_question()
    
    def show_final_score(self):
        final_score_percentage = (self.score / len(self.questions)) * 100
        messagebox.showinfo("Quiz Complete", 
                          f"Quiz finished!\nFinal Score: {self.score}/{len(self.questions)}\n"
                          f"Percentage: {final_score_percentage:.1f}%")
        self.question_frame.grid_remove()
    
    def __del__(self):
        # Close database connection when object is destroyed
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApplication(root)