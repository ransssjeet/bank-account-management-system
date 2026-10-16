
from decimal import Decimal, InvalidOperation

from bank import Bank
from storage import CSVStorage


def read_amount(prompt):
    while True:
        try:
            amount = Decimal(input(prompt).strip())
            if not amount.is_finite() or amount <= 0:
                print("Enter an amount greater than zero.")
            elif amount != amount.quantize(Decimal("0.01")):
                print("Use no more than two decimal places.")
            else:
                return amount
        except InvalidOperation:
            print("Invalid amount. Example: 100 or 100.50")

def main():
    bank = Bank(CSVStorage("data/accounts.csv", "data/transactions.csv"))
    bank.load_data()
    while True:
        print("\n=== BANK ACCOUNT MANAGEMENT SYSTEM ===")
        print("1 Create account\n2 Deposit money\n3 Withdraw money")
        print("4 Check balance\n5 Display all accounts")
        print("6 Transaction history\n7 Save data\n0 Exit")
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                name = input("Account holder name: ").strip()
                number = input("Choose account number: ").strip()
                amount = read_amount("Opening deposit: Rs. ")
                kind = input("Account type (savings/current) [savings]: ").strip().lower() or "savings"
                bank.create_account(name, number, amount, kind)
                print("Account created.")
            elif choice == "2":
                bank.deposit(input("Account number: ").strip(), read_amount("Deposit: Rs. "))
                print("Deposit successful.")
            elif choice == "3":
                bank.withdraw(input("Account number: ").strip(), read_amount("Withdraw: Rs. "))
                print("Withdrawal successful.")
            elif choice == "4":
                account = bank.get_account(input("Account number: ").strip())
                print(f"Holder: {account.owner}\nNumber: {account.account_number}")
                print(f"Type: {account.account_type}\nBalance: Rs. {account.balance:.2f}")
            elif choice == "5":
                bank.display_accounts()
            elif choice == "6":
                number = input("Account number (Enter for all): ").strip()
                bank.display_transactions(number or None)
            elif choice == "7":
                bank.save_data()
                print("Data saved.")
            elif choice == "0":
                bank.save_data()
                print("Data saved. Goodbye!")
                break
            else:
                print("Choose a valid menu option.")
        except (ValueError, KeyError, OSError) as error:
            print(f"Error: {error}")

if __name__ == "__main__":
    main()
