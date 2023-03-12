# Finance Tracker

## This is a Python application for tracking personal finances. It uses object-oriented programming (OOP) concepts and SQLite database to manage accounts, transactions, and budgets.

## Getting Started
### Install Python 3.x on your machine.
### Clone the repository: git clone https://github.com/abdul-rahman-amer/finance-tracker.git
### Create a virtual environment: python -m venv venv
### Activate the virtual environment: source venv/bin/activate (for Linux/Mac) or venv\Scripts\activate (for Windows)
### Install the required packages: pip install -r requirements.txt
### Run the application: python app.py
### Usage
### The application provides the following features:

## Create and manage accounts
### Deposit and withdraw funds
### View account statements
### Set and track budgets
### Analyze spending
### To use the application, follow these steps:

## Create an account: Account(name, balance)
### Deposit funds: account.deposit(amount, category, description)
### Withdraw funds: account.withdraw(amount, category, description)
### View account statement: account.get_statement(start_date, end_date)
### Set a budget: Budget(account, category, limit)
### Track remaining budget: budget.get_remaining(start_date, end_date)
### Analyze spending: account.analyze_spending(start_date, end_date)
### Contributing
### Contributions are welcome! If you find a bug or have a feature request, please open an issue or submit a pull request.

## Future Improvements
### This code could be improved by:

### Adding input validation and error handling
### Adding more advanced budget tracking features, such as rollover budgets or rollover transaction categories.
### Adding a user interface to make the application more user-friendly.