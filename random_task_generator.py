import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random
from datetime import datetime

class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator - Генератор случайных задач")
        self.root.geometry("750x600")
        
        # Предопределённые задачи с категориями
        self.default_tasks = [
            {"task": "Прочитать статью", "category": "Учёба"},
            {"task": "Сделать зарядку", "category": "Спорт"},
            {"task": "Пробежка 5 км", "category": "Спорт"},
            {"task": "Выучить 10 новых слов", "category": "Учёба"},
            {"task": "Сходить в спортзал", "category": "Спорт"},
            {"task": "Написать код", "category": "Работа"},
            {"task": "Проверить почту", "category": "Работа"},
            {"task": "Прочитать книгу", "category": "Учёба"},
            {"task": "Сделать план на день", "category": "Работа"},
            {"task": "Помыть посуду", "category": "Дом"},
            {"task": "Позвонить родителям", "category": "Личное"},
            {"task": "Медитация", "category": "Спорт"},
            {"task": "Посмотреть вебинар", "category": "Учёба"},
            {"task": "Сделать отчёт", "category": "Работа"},
        ]
        
        self.categories = ["Все", "Учёба", "Спорт", "Работа", "Дом", "Личное"]
        
        # Хранилище истории
        self.history = []
        self.current_filter = "Все"
        
        # Загрузка данных при старте
        self.load_from_file()
        
        # Создание интерфейса
        self.create_input_frame()
        self.create_task_frame()
        self.create_history_frame()
        self.create_filter_frame()
        self.create_button_frame()
        
    def create_input_frame(self):
        """Фрейм для добавления новых задач"""
        input_frame = ttk.LabelFrame(self.root, text="Добавить новую задачу", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(input_frame, text="Задача:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.new_task_entry = ttk.Entry(input_frame, width=40)
        self.new_task_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Категория:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.new_category_var = tk.StringVar()
        self.new_category_combo = ttk.Combobox(input_frame, textvariable=self.new_category_var, 
                                                values=self.categories[1:], width=15)
        self.new_category_combo.grid(row=0, column=3, padx=5, pady=5)
        self.new_category_combo.set("Выберите категорию")
        
        ttk.Button(input_frame, text="Добавить задачу", command=self.add_new_task).grid(row=1, column=1, columnspan=2, pady=5)
        
    def create_task_frame(self):
        """Фрейм для отображения сгенерированной задачи"""
        task_frame = ttk.LabelFrame(self.root, text="Случайная задача", padding=10)
        task_frame.pack(fill="x", padx=10, pady=5)
        
        self.task_label = tk.Label(task_frame, text="Нажмите кнопку для генерации", 
                                    font=("Arial", 16, "bold"), fg="blue", wraplength=600)
        self.task_label.pack(pady=10)
        
        self.category_label = tk.Label(task_frame, text="", font=("Arial", 10), fg="gray")
        self.category_label.pack()
        
        ttk.Button(task_frame, text="Сгенерировать задачу", command=self.generate_random_task, width=25).pack(pady=10)
        
    def create_history_frame(self):
        """Фрейм для отображения истории"""
        history_frame = ttk.LabelFrame(self.root, text="История задач", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        columns = ("date", "task", "category")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=10)
        
        self.tree.heading("date", text="Дата и время")
        self.tree.heading("task", text="Задача")
        self.tree.heading("category", text="Категория")
        
        self.tree.column("date", width=150)
        self.tree.column("task", width=400)
        self.tree.column("category", width=100)
        
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_filter_frame(self):
        """Фрейм для фильтрации"""
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Фильтр по категории:").pack(side="left", padx=5)
        
        self.filter_var = tk.StringVar(value="Все")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, values=self.categories, width=15, state="readonly")
        filter_combo.pack(side="left", padx=5)
        filter_combo.bind("<<ComboboxSelected>>", self.filter_history)
        
        ttk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter).pack(side="left", padx=20)
        
        self.total_label = ttk.Label(filter_frame, text=f"Всего задач в истории: 0", font=("Arial", 10))
        self.total_label.pack(side="right", padx=10)
        
    def create_button_frame(self):
        """Фрейм с кнопками управления"""
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(button_frame, text="Сохранить историю в JSON", command=self.save_to_file).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Загрузить историю из JSON", command=self.load_from_file).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Очистить историю", command=self.clear_history).pack(side="left", padx=5)
        
        self.status_label = ttk.Label(button_frame, text="Готов", relief="sunken")
        self.status_label.pack(side="right", padx=5, fill="x", expand=True)
        
    def get_all_tasks(self):
        """Объединение стандартных задач и пользовательских"""
        all_tasks = self.default_tasks.copy()
        existing_tasks = [t["task"] for t in all_tasks]
        
        for task in self.history:
            if task["task"] not in existing_tasks:
                all_tasks.append({"task": task["task"], "category": task["category"]})
                existing_tasks.append(task["task"])
        return all_tasks
        
    def generate_random_task(self):
        """Генерация случайной задачи"""
        all_tasks = self.get_all_tasks()
        
        if self.current_filter != "Все":
            filtered_tasks = [t for t in all_tasks if t["category"] == self.current_filter]
        else:
            filtered_tasks = all_tasks
            
        if not filtered_tasks:
            messagebox.showwarning("Предупреждение", f"Нет задач в категории '{self.current_filter}'")
            return
            
        random_task = random.choice(filtered_tasks)
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        history_entry = {
            "date": now,
            "task": random_task["task"],
            "category": random_task["category"]
        }
        
        self.history.append(history_entry)
        
        self.task_label.config(text=random_task["task"])
        self.category_label.config(text=f"Категория: {random_task['category']}")
        
        self.update_history_display()
        self.update_total_label()
        
        self.status_label.config(text=f"Сгенерирована задача: {random_task['task']}")
        
    def update_history_display(self):
        """Обновление отображения истории"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        filtered_history = self.history if self.current_filter == "Все" else [h for h in self.history if h["category"] == self.current_filter]
            
        for entry in filtered_history:
            self.tree.insert("", "end", values=(
                entry["date"],
                entry["task"],
                entry["category"]
            ))
            
    def filter_history(self, event=None):
        """Фильтрация истории по категории"""
        selected_filter = self.filter_var.get()
        self.current_filter = selected_filter if selected_filter != "Все" else "Все"
        self.update_history_display()
        self.status_label.config(text=f"Фильтр по категории: {self.current_filter}")
        
    def reset_filter(self):
        """Сброс фильтрации"""
        self.filter_var.set("Все")
        self.current_filter = "Все"
        self.update_history_display()
        self.status_label.config(text="Фильтр сброшен")
        
    def add_new_task(self):
        """Добавление новой задачи"""
        new_task = self.new_task_entry.get().strip()
        category = self.new_category_var.get().strip()
        
        if not new_task:
            messagebox.showerror("Ошибка", "Введите задачу!")
            return
            
        if not category or category == "Выберите категорию":
            messagebox.showerror("Ошибка", "Выберите категорию!")
            return
        
        # Проверка на дубликат
        for task in self.default_tasks:
            if task["task"].lower() == new_task.lower():
                messagebox.showwarning("Предупреждение", "Такая задача уже существует!")
                return
            
        new_task_dict = {"task": new_task, "category": category}
        self.default_tasks.append(new_task_dict)
        
        self.new_task_entry.delete(0, tk.END)
        self.new_category_combo.set("Выберите категорию")
        
        messagebox.showinfo("Успех", f"Задача '{new_task}' добавлена в категорию '{category}'")
        self.status_label.config(text=f"Добавлена новая задача: {new_task}")
        
    def update_total_label(self):
        """Обновление счётчика задач в истории"""
        self.total_label.config(text=f"Всего задач в истории: {len(self.history)}")
        
    def save_to_file(self):
        """Сохранение в JSON файл"""
        filename = "task_history.json"
        try:
            data = {
                "history": self.history,
                "default_tasks": self.default_tasks
            }
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.status_label.config(text=f"Сохранено в {filename}")
            messagebox.showinfo("Успех", f"Данные сохранены в {filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")
            
    def load_from_file(self):
        """Загрузка из JSON файла"""
        filename = "task_history.json"
        if not os.path.exists(filename):
            messagebox.showwarning("Предупреждение", f"Файл {filename} не найден")
            return
            
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    messagebox.showwarning("Предупреждение", "Файл пуст")
                    return
                data = json.loads(content)
                self.history = data.get("history", [])
                self.default_tasks = data.get("default_tasks", self.default_tasks)
            self.update_history_display()
            self.update_total_label()
            self.status_label.config(text=f"Загружено из {filename}")
            messagebox.showinfo("Успех", f"Загружено {len(self.history)} задач из истории")
        except json.JSONDecodeError:
            messagebox.showerror("Ошибка", "Файл JSON повреждён!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить: {e}")
            
    def clear_history(self):
        """Очистка всей истории"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить ВСЮ историю?"):
            self.history = []
            self.update_history_display()
            self.update_total_label()
            self.task_label.config(text="Нажмите кнопку для генерации")
            self.category_label.config(text="")
            self.status_label.config(text="История очищена")

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()
