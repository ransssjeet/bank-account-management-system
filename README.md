# Bleep Project 03 — Bank Account Management System

A beginner-friendly Python console project using OOP.

## Features
- Create savings and current accounts
- Deposit and withdraw money
- Check balance and display accounts
- Maintain transaction history
- Save and reload records using CSV files
- Validate input and handle common errors

## OOP concepts
- Classes and objects: `Bank`, `BankAccount`, `SavingsAccount`, `CurrentAccount`, `CSVStorage`
- Encapsulation: private attributes such as `__balance`
- Inheritance: savings/current accounts inherit from `BankAccount`
- Abstraction: `BankAccount` uses `ABC` and `@abstractmethod`
- Polymorphism: account types implement their own `account_type`
- File handling: CSV reading/writing
- Exception handling: invalid input and missing accounts

## Run
Requires Python 3.10 or newer. No third-party packages needed.

From this folder, run:

```bash
python main.py
```

The `data` CSV files are created automatically when saving.

Educational example only; it is not real banking software.
