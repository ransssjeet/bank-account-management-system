
import csv
from pathlib import Path


class CSVStorage:
    ACCOUNT_FIELDS = ("account_number", "owner", "account_type", "balance")
    TRANSACTION_FIELDS = (
        "date_time",
        "account_number",
        "transaction_type",
        "amount",
        "balance_after",
    )


    def __init__(self, accounts_file, transactions_file):
        self.__accounts_path = Path(accounts_file)
        self.__transactions_path = Path(transactions_file)

    def _read(self, path, fields):
        if not path.exists():
            return []
        with path.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            if not reader.fieldnames:
                return []
            missing = set(fields) - set(reader.fieldnames)
            if missing:
                raise ValueError(f"{path} is missing columns: {', '.join(sorted(missing))}")
            return [{key: (row.get(key) or "").strip() for key in fields} for row in reader]

    def load_all(self):
        return (self._read(self.__accounts_path, self.ACCOUNT_FIELDS),
                self._read(self.__transactions_path, self.TRANSACTION_FIELDS))

    def save_accounts(self, accounts):
        self.__accounts_path.parent.mkdir(parents=True, exist_ok=True)
        with self.__accounts_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.ACCOUNT_FIELDS)
            writer.writeheader()
            for account in accounts:
                writer.writerow({
                    "account_number": account.account_number,
                    "owner": account.owner,
                    "account_type": account.account_type,
                    "balance": f"{account.balance:.2f}",
                })

    def save_transactions(self, transactions):
        self.__transactions_path.parent.mkdir(parents=True, exist_ok=True)
        with self.__transactions_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.TRANSACTION_FIELDS)
            writer.writeheader()
            writer.writerows(transactions)
