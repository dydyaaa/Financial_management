import unittest
from unittest.mock import patch
from io import StringIO
import datetime
import json
import os
from main import *

class TestFinanceManager(unittest.TestCase):

    def setUp(self):
        self.expenses = [
            {'date': '01-01-2024', 'category': 'Доход', 'amount': 5000.0, 'description': 'Зарплата'},
            {'date': '02-01-2024', 'category': 'Расход', 'amount': -1000.0, 'description': 'Продукты'}
        ]

    def test_add_record(self):
        with patch('builtins.input', side_effect=['0', 'Доход', '2000', 'Продажа книг']):
            add_record(self.expenses)
            self.assertEqual(len(self.expenses), 3)

    def test_delete_record(self):
        with patch('builtins.input', return_value='1'):
            delete_record(self.expenses)
            self.assertEqual(len(self.expenses), 1)

    def test_balance_display(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            balance_display(self.expenses)
            self.assertIn('баланс', fake_out.getvalue())

    def test_edit_record(self):
        with patch('builtins.input', side_effect=['1', '02-01-2024', 'Расход', '1500', 'Еда']):
            edit_record(self.expenses)
            self.assertEqual(self.expenses[0]['description'], 'Еда')

    def test_income_display(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            income_display(self.expenses)
            self.assertIn('Доход', fake_out.getvalue())

    def test_expenses_display(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            expenses_display(self.expenses)
            self.assertIn('Расход', fake_out.getvalue())

    def test_search(self):
        with patch('builtins.input', side_effect=['3', '<10000']), patch('sys.stdout', new=StringIO()) as fake_out:
            search(self.expenses)
            self.assertIn('Доход', fake_out.getvalue())


    def test_display_all(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            display_all(self.expenses)
            self.assertIn('Зарплата', fake_out.getvalue())

    def test_save_and_load_expenses(self):
        save_expenses(self.expenses)
        loaded_expenses = load_expenses()
        self.assertEqual(len(loaded_expenses), 2)

if __name__ == '__main__':
    unittest.main()
