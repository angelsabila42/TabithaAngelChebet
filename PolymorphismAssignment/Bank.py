# Lab 1 Exercise 1: Create a method overloading and overriding the completes a banking system
# The parent class must be Transaction and the child class can be deposit, withdrwal and Transfer.
# Demonstrate an employer depositing, withdrawing and transfering funds.

class BankAccount:
    def __init__(self, account_holder, balance=0):
        self.balance = balance
        self.account_holder = account_holder
        
    def show_balance(self):
        print(f"{self.account_holder} Current Balance: UGX {self.balance:,}")
        
class Transaction:
    def __init__(self, account):
        self.account = account
        
    def get_transaction_type(self):
        return "Generic Transaction"
        
    def process(self, amount, note=""):
        if note:
            print(f"{self.get_transaction_type()} of UGX {amount:,} for {note}")
        else:
            print(f"{self.get_transaction_type()} of UGX {amount:,}")
        return self.account.balance
    
class Deposit(Transaction):
    def get_transaction_type(self):
        return "Deposit"
    
    def process(self, amount, note=""):
        self.account.balance += amount
        balance = super().process(amount, note)
        print(f"New balance after deposit: UGX {balance:,}")
        return balance
    
class Withdraw(Transaction):
    def get_transaction_type(self):
        return "Withdraw"
    
    def process(self, amount, note=""):
        if amount > self.account.balance:
            print("You have insufficient balance")
            return self.account.balance
        
        self.account.balance -= amount
        balance = super().process(amount, note)
        
        print(f"New balance after withdrawal is: UGX {balance:,}")
        return balance
    
class Transfer(Transaction):
    def get_transaction_type(self):
        return "Transfer"
    
    def process(self, amount, target_account, note=""):
        if amount > self.account.balance:
            print("You have insufficient balance to make this transaction")
            return self.account.balance
        
        self.account.balance -= amount
        target_account.balance += amount
        
        if note:
            print(f"{self.get_transaction_type()} of UGX {amount:,} to {target_account.account_holder} for {note}")
        else:
            print(f"{self.get_transaction_type()} of UGX {amount:,} to {target_account.account_holder}")

        return self.account.balance
    
if __name__ == "__main__":
    employer_account = BankAccount("Employer", 1500000)
    recipient_account = BankAccount("Importers", 0)

    employer_account.show_balance()

    deposit = Deposit(employer_account)
    deposit.process(1000000, "Salary")
    print()

    transfer = Transfer(employer_account)
    transfer.process(2000000, recipient_account, "Shipment Payment")
    recipient_account.show_balance()
    print()

    withdraw = Withdraw(employer_account)
    withdraw.process(200000)