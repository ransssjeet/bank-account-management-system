from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal

class BankAccount(ABC):
    """Abstract parent class for bank accounts."""
    def __init__(self, owner, account_number, balance):
        owner = owner.strip()
        account_number = account_number.strip()
        if not owner:
            raise ValueError("Name cannot be blank.")
        if not account_number:
            raise ValueError("Account number cannot be blank.")
        if balance < 0:
            raise ValueError("Balance cannot be negative.")
        self.__owner = owner
        self.__account_number = account_number
        self.__balance = balance.quantize(Decimal("0.01"))
        self.__transactions = []

    @property
    def owner(self):
        return self.__owner

    @property
    def account_number(self):
        return self.__account_number

    @property
    def balance(self):
        return self.__balance

    @property
    @abstractmethod
    def account_type(self):
        """Child classes must specify their account type."""

    @property
    def transactions(self):
        return [item.copy() for item in self.__transactions]

    def _validate_amount(self, amount):
        if not amount.is_finite() or amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if amount != amount.quantize(Decimal("0.01")):
            raise ValueError("Amount can have at most two decimal places.")

    def deposit(self, amount):
        self._validate_amount(amount)
        self.__balance += amount
        self._record("DEPOSIT", amount)

    def withdraw(self, amount):
        self._validate_amount(amount)
        if amount > self.__balance:
            raise ValueError("Insufficient balance.")
        self.__balance -= amount
        self._record("WITHDRAWAL", amount)

    def _record(self, kind, amount):
        self.__transactions.append({
            "date_time": datetime.now().astimezone().isoformat(timespec="seconds"),
            "account_number": self.__account_number,
            "transaction_type": kind,
            "amount": f"{amount:.2f}",
            "balance_after": f"{self.__balance:.2f}",
        })

    def add_loaded_transactions(self, transactions):
        self.__transactions = [item.copy() for item in transactions]

    def get_details(self):
        return f"{self.account_type} | {self.account_number} | {self.owner} | Rs. {self.balance:.2f}"

class SavingsAccount(BankAccount):
    @property
    def account_type(self):
        return "Savings"

class CurrentAccount(BankAccount):
    @property
    def account_type(self):
        return "Current"

class Bank:
    def __init__(self, storage):
        self.__accounts = {}
        self.__storage = storage

    def create_account(self, owner, number, opening_deposit, kind="savings"):
        number = number.strip()
        if number in self.__accounts:
            raise ValueError("That account number already exists.")
        if opening_deposit <= 0:
            raise ValueError("Opening deposit must be greater than zero.")
        kind = kind.lower()
        if kind == "savings":
            account = SavingsAccount(owner, number, opening_deposit)
        elif kind == "current":
            account = CurrentAccount(owner, number, opening_deposit)
        else:
            raise ValueError("Account type must be savings or current.")
        account._record("OPENING_DEPOSIT", opening_deposit)
        self.__accounts[number] = account
        self.save_data()
        return account

    def get_account(self, number):
        number = number.strip()
        if number not in self.__accounts:
            raise KeyError("Account not found. Check the account number.")
        return self.__accounts[number]

    def deposit(self, number, amount):
        self.get_account(number).deposit(amount)
        self.save_data()

    def withdraw(self, number, amount):
        self.get_account(number).withdraw(amount)
        self.save_data()

    def display_accounts(self):
        if not self.__accounts:
            print("No accounts found.")
        for account in self.__accounts.values():
            print(account.get_details())

    def display_transactions(self, number=None):
        accounts = [self.get_account(number)] if number else list(self.__accounts.values())
        found = False
        for account in accounts:
            for item in account.transactions:
                found = True
                print(f"{item['date_time']} | {item['account_number']} | {item['transaction_type']} | Rs. {item['amount']} | Balance: Rs. {item['balance_after']}")
        if not found:
            print("No transactions found.")

    def save_data(self):
        self.__storage.save_accounts(list(self.__accounts.values()))
        transactions = [item for account in self.__accounts.values() for item in account.transactions]
        self.__storage.save_transactions(transactions)

    def load_data(self):
        accounts, transactions = self.__storage.load_all()
        grouped = {}
        for item in transactions:
            grouped.setdefault(item["account_number"], []).append(item)
        for row in accounts:
            cls = SavingsAccount if row["account_type"].lower() == "savings" else CurrentAccount
            account = cls(row["owner"], row["account_number"], Decimal(row["balance"]))
            account.add_loaded_transactions(grouped.get(account.account_number, []))
            self.__accounts[account.account_number] = account
