import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner - Планер тренировок")
        self.root.geometry("850x600")
        
        # Типы тренировок
        self.training_types = ["Бег", "Плавание", "Велосипед", "Фитнес", "Йога", "Силовая", "Растяжка"]
        
        # Хранилище тренировок
        self.trainings = []
        self.current_filter = "all"
        self.filter_type_value = "Все"
        self.filter_date_value = ""
        
        self.load_from_file()
        
        self.create_input_frame()
        self.create_list_frame()
        self.create_filter_frame()
        self.create_button_frame()
        
    def create_input_frame(self):
        input_frame = ttk.LabelFrame(self.root, text="Добавить тренировку", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Поле Дата
        ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.date_entry = ttk.Entry(input_frame, width=15)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Поле Тип тренировки
        ttk.Label(input_frame, text="Тип тренировки:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(input_frame, textvariable=self.type_var, values=self.training_types, width=15)
        self.type_combo.grid(row=0, column=3, padx=5, pady=5)
        self.type_combo.set("Выберите тип")
        
        # Поле Длительность
        ttk.Label(input_frame, text="Длительность (мин):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.duration_entry = ttk.Entry(input_frame, width=15)
        self.duration_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Кнопка добавления
        ttk.Button(input_frame, text="Добавить тренировку", command=self.add_training).grid(row=1, column=2, columnspan=2, pady=5)
        
    def create_filter_frame(self):
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        # Фильтр по типу тренировки
        ttk.Label(filter_frame, text="Фильтр по типу:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_type = ttk.Combobox(filter_frame, values=["Все"] + self.training_types, width=15)
        self.filter_type.grid(row=0, column=1, padx=5, pady=5)
        self.filter_type.set("Все")
        ttk.Button(filter_frame, text="Применить", command=self.filter_by_type).grid(row=0, column=2, padx=5)
        
        # Фильтр по дате
        ttk.Label(filter_frame, text="Фильтр по дате:").grid(row=1, column=0, padx=5, pady=5)
        self.filter_date = ttk.Entry(filter_frame, width=15)
        self.filter_date.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(filter_frame, text="Применить", command=self.filter_by_date).grid(row=1, column=2, padx=5)
        
        # Кнопка сброса
        ttk.Button(filter_frame, text="Сбросить фильтры", command=self.reset_filter).grid(row=2, column=0, columnspan=3, pady=5)
        
        # Статистика
        self.stats_label = ttk.Label(filter_frame, text="", font=("Arial", 10))
        self.stats_label.grid(row=3, column=0, columnspan=3, pady=5)
        self.update_stats()
        
    def create_list_frame(self):
        list_frame = ttk.LabelFrame(self.root, text="Список тренировок", padding=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        columns = ("date", "type", "duration")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
        
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип тренировки")
        self.tree.heading("duration", text="Длительность (мин)")
        
        self.tree.column("date", width=120)
        self.tree.column("type", width=150)
        self.tree.column("duration", width=120)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_button_frame(self):
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(button_frame, text="Сохранить в JSON", command=self.save_to_file).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Загрузить из JSON", command=self.load_from_file).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Очистить всё", command=self.clear_all).pack(side="left", padx=5)
        
        self.status_label = ttk.Label(button_frame, text="Готов", relief="sunken")
        self.status_label.pack(side="right", padx=5, fill="x", expand=True)
        
    def validate_date(self, date_str):
        """Проверка корректности даты"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
            
    def validate_duration(self, duration_str):
        """Проверка длительности (положительное число)"""
        try:
            duration = float(duration_str)
            return duration > 0
        except ValueError:
            return False
            
    def add_training(self):
        date = self.date_entry.get().strip()
        training_type = self.type_var.get().strip()
        duration = self.duration_entry.get().strip()
        
        # Валидация даты
        if not self.validate_date(date):
            messagebox.showerror("Ошибка", "Неверный формат даты!\nИспользуйте ГГГГ-ММ-ДД")
            return
            
        # Валидация типа тренировки
        if not training_type or training_type == "Выберите тип":
            messagebox.showerror("Ошибка", "Выберите тип тренировки!")
            return
            
        # Валидация длительности
        if not self.validate_duration(duration):
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом!")
            return
            
        training = {
            "date": date,
            "type": training_type,
            "duration": float(duration)
        }
        
        self.trainings.append(training)
        self.update_display()
        self.update_stats()
        
        # Очистка полей
        self.type_combo.set("Выберите тип")
        self.duration_entry.delete(0, tk.END)
        
        self.status_label.config(text=f"Добавлена тренировка: {training_type} - {duration} мин")
        
    def update_display(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        filtered_trainings = self.get_filtered_trainings()
        
        for training in filtered_trainings:
            self.tree.insert("", "end", values=(
                training["date"],
                training["type"],
                f"{training['duration']:.0f}"
            ))
            
        self.status_label.config(text=f"Показано тренировок: {len(filtered_trainings)} из {len(self.trainings)}")
        
    def get_filtered_trainings(self):
        result = self.trainings
        
        if self.current_filter == "by_type":
            result = [t for t in result if t["type"] == self.filter_type_value]
        elif self.current_filter == "by_date":
            result = [t for t in result if t["date"] == self.filter_date_value]
        elif self.current_filter == "both":
            result = [t for t in result if t["type"] == self.filter_type_value]
            result = [t for t in result if t["date"] == self.filter_date_value]
            
        return result
        
    def filter_by_type(self):
        training_type = self.filter_type.get()
        if training_type == "Все":
            self.reset_filter()
            return
            
        self.filter_type_value = training_type
        
        if self.current_filter == "by_date":
            self.current_filter = "both"
        else:
            self.current_filter = "by_type"
            
        self.update_display()
        self.status_label.config(text=f"Фильтр по типу: {training_type}")
        
    def filter_by_date(self):
        date = self.filter_date.get().strip()
        
        if not date:
            messagebox.showwarning("Предупреждение", "Введите дату для фильтрации")
            return
            
        if not self.validate_date(date):
            messagebox.showerror("Ошибка", "Неверный формат даты!")
            return
            
        self.filter_date_value = date
        
        if self.current_filter == "by_type":
            self.current_filter = "both"
        else:
            self.current_filter = "by_date"
            
        self.update_display()
        self.status_label.config(text=f"Фильтр по дате: {date}")
        
    def reset_filter(self):
        self.current_filter = "all"
        self.filter_type.set("Все")
        self.filter_date.delete(0, tk.END)
        self.filter_type_value = "Все"
        self.filter_date_value = ""
        self.update_display()
        self.status_label.config(text="Фильтры сброшены")
        
    def update_stats(self):
        if not self.trainings:
            self.stats_label.config(text="Всего тренировок: 0 | Общее время: 0 мин")
            return
            
        total_duration = sum(t["duration"] for t in self.trainings)
        self.stats_label.config(text=f"Всего тренировок: {len(self.trainings)} | Общее время: {total_duration:.0f} мин")
        
    def save_to_file(self):
        filename = "trainings.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.trainings, f, ensure_ascii=False, indent=2)
            self.status_label.config(text=f"Сохранено в {filename}")
            messagebox.showinfo("Успех", f"Данные сохранены в {filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")
            
    def load_from_file(self):
        filename = "trainings.json"
        if not os.path.exists(filename):
            messagebox.showwarning("Предупреждение", f"Файл {filename} не найден")
            return
            
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    messagebox.showwarning("Предупреждение", "Файл пуст")
                    self.trainings = []
                else:
                    self.trainings = json.loads(content)
            self.reset_filter()
            self.update_stats()
            self.status_label.config(text=f"Загружено из {filename}")
            messagebox.showinfo("Успех", f"Загружено {len(self.trainings)} тренировок")
        except json.JSONDecodeError:
            messagebox.showerror("Ошибка", "Файл JSON повреждён!")
            self.trainings = []
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить: {e}")
            
    def clear_all(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить ВСЕ тренировки?"):
            self.trainings = []
            self.reset_filter()
            self.update_stats()
            self.status_label.config(text="Все тренировки удалены")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
