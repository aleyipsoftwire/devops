from bank_api.bank import Bank

class BankReport:

    def __init__(self, bank: Bank):
        self.bank = bank

    def get_balance(self, name: str): 
        transactions = self.bank.get_transactions_for_account(name)

        total = 0
        for transaction in transactions:
            total += transaction.amount

        return total
