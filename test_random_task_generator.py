import unittest
import random
from datetime import datetime

class TestRandomTaskGenerator(unittest.TestCase):
    
    def setUp(self):
        self.default_tasks = [
            {"task": "Прочитать статью", "category": "Учёба"},
            {"task": "Сделать зарядку", "category": "Спорт"},
            {"task": "Пробежка 5 км", "category": "Спорт"},
            {"task": "Выучить 10 новых слов", "category": "Учёба"},
            {"task": "Написать код", "category": "Работа"},
        ]
        self.categories = ["Учёба", "Спорт", "Работа", "Дом", "Личное"]
        
    def test_validate_task_not_empty(self):
        """Проверка задачи (не должна быть пустой)"""
        def is_valid_task(task):
            return bool(task and task.strip())
        
        self.assertTrue(is_valid_task("Прочитать книгу"))
        self.assertTrue(is_valid_task("  Сделать зарядку  "))
        self.assertFalse(is_valid_task(""))
        self.assertFalse(is_valid_task("   "))
        
    def test_validate_category(self):
        """Проверка категории (должна быть из списка)"""
        def is_valid_category(category):
            return category in self.categories
        
        self.assertTrue(is_valid_category("Учёба"))
        self.assertTrue(is_valid_category("Спорт"))
        self.assertTrue(is_valid_category("Работа"))
        self.assertFalse(is_valid_category(""))
        self.assertFalse(is_valid_category("Хобби"))
        self.assertFalse(is_valid_category(" "))
        
    def test_generate_random_task(self):
        """Проверка генерации случайной задачи"""
        def generate_random_task(tasks):
            return random.choice(tasks)
        
        task1 = generate_random_task(self.default_tasks)
        task2 = generate_random_task(self.default_tasks)
        
        self.assertIn(task1, self.default_tasks)
        self.assertIn(task2, self.default_tasks)
        
    def test_filter_by_category(self):
        """Проверка фильтрации по категории"""
        history = [
            {"task": "Чтение", "category": "Учёба"},
            {"task": "Бег", "category": "Спорт"},
            {"task": "Код", "category": "Работа"},
            {"task": "Книга", "category": "Учёба"},
        ]
        
        def filter_by_category(history, category):
            return [h for h in history if h["category"] == category]
        
        result = filter_by_category(history, "Учёба")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["task"], "Чтение")
        self.assertEqual(result[1]["task"], "Книга")
        
        result = filter_by_category(history, "Спорт")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["task"], "Бег")
        
        result = filter_by_category(history, "Дом")
        self.assertEqual(len(result), 0)
        
    def test_add_new_task(self):
        """Проверка добавления новой задачи"""
        tasks = self.default_tasks.copy()
        
        def add_new_task(tasks, new_task, category):
            tasks.append({"task": new_task, "category": category})
            return tasks
        
        tasks = add_new_task(tasks, "Помыть посуду", "Дом")
        
        self.assertEqual(len(tasks), 6)
        self.assertEqual(tasks[-1]["task"], "Помыть посуду")
        self.assertEqual(tasks[-1]["category"], "Дом")
        
    def test_task_uniqueness_check(self):
        """Проверка уникальности добавляемой задачи"""
        tasks = self.default_tasks.copy()
        
        def is_unique_task(tasks, new_task):
            return new_task.lower() not in [t["task"].lower() for t in tasks]
        
        self.assertFalse(is_unique_task(tasks, "Прочитать статью"))
        self.assertTrue(is_unique_task(tasks, "Новая задача"))
        
    def test_history_entry_has_date(self):
        """Проверка что запись истории содержит дату"""
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "task": "Тест",
            "category": "Учёба"
        }
        
        self.assertIn("date", entry)
        self.assertIsNotNone(entry["date"])
        self.assertTrue(len(entry["date"]) > 0)

if __name__ == "__main__":
    unittest.main()
