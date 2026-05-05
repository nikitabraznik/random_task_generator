import unittest
from datetime import datetime

class TestTrainingPlanner(unittest.TestCase):
    
    def test_validate_date(self):
        """Проверка формата даты"""
        def validate_date(date_str):
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return True
            except ValueError:
                return False
        
        self.assertTrue(validate_date("2026-05-05"))
        self.assertTrue(validate_date("2024-12-31"))
        self.assertFalse(validate_date("05.05.2026"))
        self.assertFalse(validate_date("2026/05/05"))
        self.assertFalse(validate_date(""))
        
    def test_validate_duration_positive(self):
        """Проверка длительности (положительное число)"""
        def validate_duration(duration_str):
            try:
                duration = float(duration_str)
                return duration > 0
            except ValueError:
                return False
        
        self.assertTrue(validate_duration("30"))
        self.assertTrue(validate_duration("45.5"))
        self.assertTrue(validate_duration("15"))
        self.assertFalse(validate_duration("0"))
        self.assertFalse(validate_duration("-10"))
        self.assertFalse(validate_duration("abc"))
        self.assertFalse(validate_duration(""))
        
    def test_filter_by_type(self):
        """Проверка фильтрации по типу тренировки"""
        trainings = [
            {"type": "Бег", "duration": 30},
            {"type": "Плавание", "duration": 45},
            {"type": "Бег", "duration": 20},
            {"type": "Йога", "duration": 60},
        ]
        
        def filter_by_type(trainings, training_type):
            return [t for t in trainings if t["type"] == training_type]
        
        result = filter_by_type(trainings, "Бег")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["duration"], 30)
        self.assertEqual(result[1]["duration"], 20)
        
        result = filter_by_type(trainings, "Плавание")
        self.assertEqual(len(result), 1)
        
        result = filter_by_type(trainings, "Фитнес")
        self.assertEqual(len(result), 0)
        
    def test_filter_by_date(self):
        """Проверка фильтрации по дате"""
        trainings = [
            {"date": "2026-05-01", "duration": 30},
            {"date": "2026-05-02", "duration": 45},
            {"date": "2026-05-01", "duration": 20},
        ]
        
        def filter_by_date(trainings, date):
            return [t for t in trainings if t["date"] == date]
        
        result = filter_by_date(trainings, "2026-05-01")
        self.assertEqual(len(result), 2)
        
        result = filter_by_date(trainings, "2026-05-02")
        self.assertEqual(len(result), 1)
        
        result = filter_by_date(trainings, "2026-06-01")
        self.assertEqual(len(result), 0)
        
    def test_calculate_total_duration(self):
        """Проверка подсчёта общего времени"""
        trainings = [
            {"duration": 30},
            {"duration": 45},
            {"duration": 20},
        ]
        
        def total_duration(trainings):
            return sum(t["duration"] for t in trainings)
        
        self.assertEqual(total_duration(trainings), 95)
        self.assertEqual(total_duration([]), 0)

if __name__ == "__main__":
    unittest.main()
