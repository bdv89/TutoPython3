import tkinter as tk
import random
import time


class MathTrainerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Trainer")
        self.root.geometry("600x400")

        # Initialize variables
        self.difficulty = 1
        self.game_mode = None
        self.start_time = None
        self.time_limit = 30  # Seconds for time-attack mode
        self.correct_count = 0
        self.total_count = 0
        self.current_answer = 0

        # Create UI
        self.create_widgets()

    def create_widgets(self):
        # Mode Selection
        tk.Label(self.root, text="Select Game Mode:").pack()
        tk.Button(self.root, text="Time Attack", command=lambda: self.start_game("time_attack")).pack()
        tk.Button(self.root, text="Endless Mode", command=lambda: self.start_game("endless")).pack()
        tk.Button(self.root, text="Challenge Mode", command=lambda: self.start_game("challenge")).pack()

        # Problem Display
        self.problem_label = tk.Label(self.root, text="", font=("Helvetica", 24))
        self.problem_label.pack(pady=20)

        # Input Field
        self.answer_entry = tk.Entry(self.root, font=("Helvetica", 18), justify="center")
        self.answer_entry.pack()
        self.answer_entry.bind("<Return>", self.check_answer)

        # Feedback and Stats
        self.feedback_label = tk.Label(self.root, text="", font=("Helvetica", 18))
        self.feedback_label.pack(pady=10)
        self.stats_label = tk.Label(self.root, text="", font=("Helvetica", 16))
        self.stats_label.pack(pady=10)

    def start_game(self, mode):
        self.game_mode = mode
        self.difficulty = 1
        self.correct_count = 0
        self.total_count = 0
        self.start_time = time.time()
        self.next_problem()

    def generate_problem(self):
        if self.difficulty == 1:
            a, b = random.randint(1, 10), random.randint(1, 10)
            operator = random.choice(["+", "-"])
        elif self.difficulty == 2:
            a, b = random.randint(10, 50), random.randint(10, 50)
            operator = random.choice(["+", "-", "*"])
        else:
            a, b = random.randint(50, 100), random.randint(1, 10)
            operator = random.choice(["+", "-", "*", "//"])

        problem = f"{a} {operator} {b}"
        self.current_answer = eval(problem)
        return problem

    def next_problem(self):
        if self.game_mode == "time_attack" and time.time() - self.start_time > self.time_limit:
            self.end_game("Time's up!")
            return
        elif self.game_mode == "challenge" and self.total_count >= 10:
            self.end_game("Challenge complete!")
            return

        self.total_count += 1
        if self.total_count % 5 == 0:
            self.difficulty += 1

        problem = self.generate_problem()
        self.problem_label.config(text=problem)
        self.feedback_label.config(text="", fg="black")
        self.answer_entry.delete(0, tk.END)

    def check_answer(self, event):
        user_answer = self.answer_entry.get()
        try:
            user_answer = int(user_answer)
        except ValueError:
            self.feedback_label.config(text="Invalid input!", fg="red")
            return

        if user_answer == self.current_answer:
            self.correct_count += 1
            self.feedback_label.config(text="Correct!", fg="green")
        else:
            self.feedback_label.config(text=f"Wrong! Correct answer was {self.current_answer}", fg="red")

        self.update_stats()
        if self.game_mode != "endless":
            self.next_problem()

    def update_stats(self):
        accuracy = (self.correct_count / self.total_count) * 100 if self.total_count else 0
        self.stats_label.config(text=f"Correct: {self.correct_count} | Total: {self.total_count} | Accuracy: {accuracy:.2f}%")

    def end_game(self, message):
        self.problem_label.config(text=message)
        self.feedback_label.config(text="")
        self.stats_label.config(text=f"Final Score: {self.correct_count}/{self.total_count}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MathTrainerApp(root)
    root.mainloop()

