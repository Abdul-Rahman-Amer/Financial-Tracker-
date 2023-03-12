import sqlite3
from datetime import datetime

class Transaction:
    def __init__(self, date, amount, category, description):
        self.date = date
        self.amount = amount
        self.category = category
        self.description = description

class Budget:
    def __init__(self, account, category, limit):
        self.account = account
        self.category = category
        self.limit = limit

    def _save_budget(self):
        with sqlite3.connect("transactions.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO budgets VALUES (?, ?, ?)", (self.account, self.category, self.limit))
            conn.commit()

    def get_remaining(self, start_date=None, end_date=None):
        with sqlite3.connect("transactions.db") as conn:
            cursor = conn.cursor()
            if start_date and end_date:
                cursor.execute("SELECT SUM(amount) FROM transactions WHERE account = ? AND category = ? AND date BETWEEN ? AND ?", (self.account, self.category, start_date, end_date))
            elif start_date:
                cursor.execute("SELECT SUM(amount) FROM transactions WHERE account = ? AND category = ? AND date >= ?", (self.account, self.category, start_date))
            elif end_date:
                cursor.execute("SELECT SUM(amount) FROM transactions WHERE account = ? AND category = ? AND date <= ?", (self.account, self.category, end_date))
            else:
                cursor.execute("SELECT SUM(amount) FROM transactions WHERE account = ? AND category = ?", (self.account, self.category))
            row = cursor.fetchone()
        return self.limit - row[0] if row[0] else self.limit

class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def deposit(self, amount, category, description):
        self.balance += amount
        transaction = Transaction(datetime.now(), amount, category, description)
        self._save_transaction(transaction)

    def withdraw(self, amount, category, description):
        if self.balance >= amount:
            self.balance -= amount
            transaction = Transaction(datetime.now(), -amount, category, description)
            self._save_transaction(transaction)
        else:
            print("Insufficient funds")

    def _save_transaction(self, transaction):
        with sqlite3.connect("transactions.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?)", (self.name, transaction.date, transaction.amount, transaction.category, transaction.description))
            conn.commit()

    def get_statement(self, start_date=None, end_date=None):
        with sqlite3.connect("transactions.db") as conn:
            cursor = conn.cursor()
            if start_date and end_date:
                cursor.execute("SELECT * FROM transactions WHERE account = ? AND date BETWEEN ? AND ?", (self.name, start_date, end_date))
            elif start_date:
                cursor.execute("SELECT * FROM transactions WHERE account = ? AND date >= ?", (self.name, start_date))
            elif end_date:
                cursor.execute("SELECT * FROM transactions WHERE account = ? AND date <= ?", (self.name, end_date))
            else:
                cursor.execute("SELECT * FROM transactions WHERE account = ?", (self.name,))
            rows = cursor.fetchall()
        return [Transaction(*row[1:]) for row in rows]

    def analyze_spending(self, start_date=None, end_date=None):
        with sqlite3.connect("transactions.db") as conn:
            cursor = conn.cursor()
            if start_date and end_date:
                cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE account = ? AND date BETWEEN ? AND ? GROUP BY category", (self.name, start_date, end_date))
            elif start_date:
                cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE account = ? AND date >= ? GROUP BY category", (self.name, start_date))
            elif end_date:
                cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE account = ? AND date <= ? GROUP BY category", (self.name, end_date))
            else:
                cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE account = ? GROUP BY category", (self.name,))
            rows = cursor.fetchall()
        results = {}
        for row in rows:
            category = row[0]
            spent = row[1]
            budget = self._get_budget(category)
            remaining = budget.get_remaining(start_date, end_date)
            results[category] = {"spent": spent, "remaining": remaining}
        return results
