import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import ttk

class Goal:
    count = 1

    def __init__(self, name, description, target_date):
        self.id = Goal.count
        Goal.count += 1
        self.name = name
        self.description = description
        self.target_date = target_date
        self.completed = False

class User:
    def __init__(self, full_name, age):
        self.full_name = full_name
        self.age = age

class GoalTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Target Tracer")
        self.root.geometry("1700x1400")
        self.root.configure(bg='green')

        self.conn = sqlite3.connect('./goals.db')
        self.cursor = self.conn.cursor()
        self.create_goals_table()
        self.create_users_table()

        self.goals = []

        tk.Label(self.root, text="Приложение для эффективного формирования и достижения цели", height=2, font=("Arial", 20), bg='yellow').pack(pady=10)

        self.user_name_label = tk.Label(self.root, text="ФИО пользователя:", font=("Arial", 14), bg='orange')
        self.user_name_label.pack()

        self.user_name_entry = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.user_name_entry.pack()

        self.user_age_label = tk.Label(self.root, text="Возраст пользователя:", font=("Arial", 14), bg='orange')
        self.user_age_label.pack()

        self.user_age_entry = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.user_age_entry.pack()

        self.add_user_button = tk.Button(self.root, text="Добавить пользователя", command=self.add_user, font=("Arial", 14), bg='lime')
        self.add_user_button.pack()

        self.user_listbox = tk.Listbox(self.root, font=("Arial", 12), width=80, height=7)
        self.user_listbox.pack()

        self.goal_label = tk.Label(self.root, text="Название цели:", font=("Arial", 14), bg='orange')
        self.goal_label.pack()

        self.goal_entry = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.goal_entry.pack()

        self.description_label = tk.Label(self.root, text="Описание цели:", font=("Arial", 14), bg='orange')
        self.description_label.pack()

        self.description_entry = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.description_entry.pack()

        self.date_label = tk.Label(self.root, text="Дата достижения цели:", font=("Arial", 14), bg='orange')
        self.date_label.pack()

        self.date_entry = tk.Entry(self.root, width=30,  font=("Arial", 12))
        self.date_entry.pack()

        self.add_goal_button = tk.Button(self.root, text="Добавить цель", command=self.add_goal, font=("Arial", 14), bg='lime')
        self.add_goal_button.pack()

        self.goal_listbox = tk.Listbox(self.root, font=("Arial", 12), width=80, height=7)
        self.goal_listbox.pack()

        self.complete_button = tk.Button(self.root, text="Отметить цель достигнутой", command=self.complete_goal, font=("Arial", 14))
        self.complete_button.pack()

        self.remove_button = tk.Button(self.root, text="Удалить цель", command=self.remove_goal, font=("Arial", 14))
        self.remove_button.pack()

        self.show_button = tk.Button(self.root, text="Показать список целей", command=self.show_goals, font=("Arial", 14))
        self.show_button.pack()

        self.show_db_users_button = tk.Button(self.root, text="Показать список пользователей", command=self.show_users, font=("Arial", 14))
        self.show_db_users_button.pack()

        self.show_db_user_goals_button = tk.Button(self.root, text="Показать цели пользователей", command=self.show_user_goals, font=("Arial", 14))
        self.show_db_user_goals_button.pack()

    def create_goals_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS goals (
                                id INTEGER PRIMARY KEY,
                                user_id INTEGER,
                                name TEXT,
                                description TEXT,
                                target_date TEXT,
                                completed INTEGER)''')

        self.conn.commit()

    def create_users_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            full_name TEXT,
                            age INTEGER)''')
        self.conn.commit()

    def select_user(self):
        selected_index = self.user_listbox.curselection()
        if selected_index:
            user_id = selected_index[0] + 1
            return user_id
        else:
            messagebox.showinfo("Ошибка", "Выберите пользователя для добавления цели.")
            return None

    def add_user(self):
        full_name = self.user_name_entry.get()
        age = self.user_age_entry.get()
        new_user = User(full_name, age)
        self.user_listbox.insert(tk.END, f"{new_user.full_name} - {new_user.age}")
        messagebox.showinfo("Успех", "Пользователь добавлен.")
        self.add_user_to_db(full_name, age)
        self.user_name_entry.delete(0, tk.END)
        self.user_age_entry.delete(0, tk.END)

    def add_user_to_db(self, full_name, age):
        self.cursor.execute("INSERT INTO users (full_name, age) VALUES (?, ?)",
                            (full_name, age))
        self.conn.commit()

    def show_users(self):
        self.user_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT * FROM users ORDER BY id")
        rows = self.cursor.fetchall()
        for index, row in enumerate(rows, start=1):
            id, full_name, age = row
            self.user_listbox.insert(tk.END, f"{index}. {full_name} - {age}")

    def add_goal(self):
        name = self.goal_entry.get()
        description = self.description_entry.get()
        target_date = self.date_entry.get()

        user_id = self.select_user()

        if user_id is not None:
            new_goal = Goal(name, description, target_date)
            self.goals.append(new_goal)
            self.goal_listbox.insert(tk.END, f"{new_goal.id}: {name} - {description} - {target_date}")
            messagebox.showinfo("Успех", "Цель добавлена.")
            self.add_goal_to_db(user_id, name, description, target_date)
            self.goal_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)

    def add_goal_to_db(self, user_id, name, description, target_date):
        self.cursor.execute("INSERT INTO goals (user_id, name, description, target_date, completed) VALUES (?, ?, ?, ?, ?)",
                            (user_id, name, description, target_date, False))
        self.conn.commit()

    def show_goals(self):
        self.goal_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT * FROM goals")
        rows = self.cursor.fetchall()
        for row in rows:
            id, _, name, description, target_date, completed = row
            status = "[✓]" if completed else ""
            self.goal_listbox.insert(tk.END, f"{id}: {status} {name} - {description} - {target_date}")

    def complete_goal(self):
        selected_index = self.goal_listbox.curselection()
        if selected_index:
            goal_id = selected_index[0] + 1
            self.cursor.execute("UPDATE goals SET completed=? WHERE id=?", (True, goal_id))
            self.conn.commit()
            self.show_goals()
            messagebox.showinfo("Успех", f"Цель №{goal_id} достигнута!")
            self.show_user_goals()
        else:
            messagebox.showinfo("Ошибка", "Выберите цель для отметки достижения.")

    def update_goal_status_in_db(self, goal_id, completed):
        self.cursor.execute("UPDATE goals SET completed=? WHERE id=?", (True if completed else False, goal_id))
        self.conn.commit()

    def refresh_user_goals(self):
        self.show_user_goals()

    def remove_goal(self):
        selected_index = self.goal_listbox.curselection()
        if selected_index:
            goal_index = selected_index[0]
            goal_info = self.goal_listbox.get(selected_index)
            goal_id = goal_info.split(':')[0]
            self.cursor.execute("DELETE FROM goals WHERE id=?", (goal_id,))
            self.conn.commit()
            self.goal_listbox.delete(selected_index)
            messagebox.showinfo("Успех", "Цель удалена.")
        else:
            messagebox.showinfo("Ошибка", "Выберите цель для удаления.")

    def show_db_goals(self):
        self.goal_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT * FROM goals")
        rows = self.cursor.fetchall()
        for row in rows:
            id, name, description, target_date, completed = row
            status = "[✓]" if completed else ""
            self.goal_listbox.insert(tk.END, f"{id}: {status} {name} - {description} - {target_date}")

    def add_goal_for_user(self, user_id, name, description, target_date):
        self.cursor.execute("INSERT INTO goals (user_id, name, description, target_date, completed) VALUES (?, ?, ?, ?, ?)",
                            (user_id, name, description, target_date, False))
        self.conn.commit()

    def show_user_goals(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Совмещенные записи")
        new_window.geometry("1200x600")

        tree = ttk.Treeview(new_window,
                            columns=(
                            "Number", "Full Name", "Age", "Goal Name", "Description", "Target Date", "Completed"),
                            show='headings', height=100)
        tree.heading("Number", text="№")
        tree.heading("Full Name", text="ФИО пользователя")
        tree.heading("Age", text="Возраст")
        tree.heading("Goal Name", text="Название цели")
        tree.heading("Description", text="Описание цели")
        tree.heading("Target Date", text="Дата достижения цели")
        tree.heading("Completed", text="Достигнута")

        tree.column("Number", width=50)
        tree.column("Full Name", width=250)
        tree.column("Age", width=80)
        tree.column("Goal Name", width=250)
        tree.column("Description", width=250)
        tree.column("Target Date", width=150)
        tree.column("Completed", width=150)

        tree.pack()

        self.cursor.execute(
            "SELECT users.full_name, users.age, goals.name, goals.description, goals.target_date, goals.completed FROM users INNER JOIN goals ON users.id = goals.user_id")
        rows = self.cursor.fetchall()

        for index, row in enumerate(rows, start=1):
            full_name, age, goal_name, description, target_date, completed = row
            data = {'Number': index, 'Full Name': full_name, 'Age': age, 'Goal Name': goal_name,
                    'Description': description,
                    'Target Date': target_date, 'Completed': 'Да' if completed else 'Нет'}
            status = "[✓]" if completed else ""
            if completed:
                tree.insert("", "end", values=list(data.values()), tags=("completed",))
            else:
                tree.insert("", "end", values=list(data.values()))

        tree.tag_configure("completed", background="lightgreen")

        new_window.mainloop()

    def update_goal_status_in_treeview(self, tree, goal_id, completed):
        for item in tree.get_children():
            if tree.item(item)['values'][5] == goal_id:
                tree.item(item, values=(tree.item(item)['values'][0:5] + ['Да' if completed else 'Нет']))
    def update_main_window(self):
        self.show_user_goals()
def main():
    root = tk.Tk()
    app = GoalTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
