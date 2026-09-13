from pybank.accounts import Account
from pybank.exceptions import AccountNotFound, BankError, LimitExceeded
from pybank.transaction import TransactionLog, Transaction
from pybank.utils import log_operation

TRANSFER_LIMIT = 50000

class Bank:
    def __init__(self, name):
        self.name = name
        self._accounts: list[Account] = []
        self.log = TransactionLog

    def open_account(self, account) :
        self._accounts.append(account)
        return account

    def find_account(self, acc_number):
        for account in self._accounts:
            if account.acc_number == acc_number:
                return account
        raise AccountNotFound(acc_number)

    @log_operation
    def withdraw(self, number, amount):
        account = self.find_account(number)
        new_balance = account.withdraw(amount)
        self.log.add(Transaction("WITHDRAW", amount, account))
        return new_balance

    @log_operation
    def deposit(self, number, amount):
        account = self.find_account(number)
        new_balance = account.deposit(amount)
        self.log.add(Transaction("DEPOSIT", amount, account))
        return new_balance

    @log_operation
    def transfer(self, sourse, target, amount):
        if amount > TRANSFER_LIMIT:
            raise LimitExceeded(amount, TRANSFER_LIMIT)

        sourse_account = self.find_account(sourse)
        target_account = self.find_account(target)

        sourse_account.withdraw(amount)
        try:
            target_account.deposit(amount)
        except BankError as e:
            sourse_account.deposit(amount)
            raise

        self.log.add(Transaction("TRANSFER", amount, sourse, target))


    @property
    def total(self):
        return round(sum(acc.balance for acc in self._accounts), 2)

    def __len__(self):
        return len(self._accounts)

    def __iter__(self):
        return iter(self._accounts)

    def __contains__(self, item):
        if isinstance(item, Account):
            acc_number = item.acc_number
        else:
            acc_number = item

        for account in self._accounts:
            if account.acc_number == acc_number:
                return True
        return False


    def __getitem__(self, number):
        return self.find_account(number)

    def __repr__(self):
        return f"Bank('{self.name}', рахунків: {len(self)})"
