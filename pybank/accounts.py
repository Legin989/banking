from pybank.exceptions import InvalidAmount, InsufficientFunds, AccountBlocked, AccountError, LimitExceeded

class Account:

    _counter = 0

    def __init__(self, owner:str, balance:float = 0 ):
        Account._counter += 1
        self.acc_number = f"ACC{Account._counter:03d}"
        self.owner = owner
        self._balance = balance
        self.is_blocked = False

    @classmethod
    def reset_counter(cls):
        Account._counter = 0

    @property
    def balance(self):
        return round(self._balance, 2)

    @property
    def available(self):
        return round(self._balance, 2)

    @property
    def kind(self):
        return "Базовий"

    @staticmethod
    def validate_amount(amount:float):
        if not isinstance(amount, (int, float)) or amount < 0:
            raise InvalidAmount(amount)

    def block_account(self):
        self.is_blocked = True

    def deposit(self, amount:float) -> float:
        if self.is_blocked:
            raise AccountBlocked(self.acc_number)
        self.validate_amount(amount)
        self._balance += amount
        return self.balance

    def withdraw(self, amount:float) -> float:
        if self.is_blocked:
            raise AccountBlocked(self.acc_number)
        self.validate_amount(amount)

        if self._balance < amount:
            raise InsufficientFunds(self.acc_number, self._balance, amount)

        self._balance -= amount
        return self.balance

    # def transfer(self, to:"Account", amount:float ) -> float:
    #     if not isinstance(to, Account):
    #         raise AccountError()
    #     self.withdraw(amount)
    #     to.deposit(amount)

    def to_dict(self):
        return {
            "type": type(self).__name__,
            "acc_number": self.acc_number,
            "owner":self.owner,
            "balance": self.balance,
            "is_blocked": self.is_blocked,
        }

    @classmethod
    def from_dict(cls, data):
        account = cls(data["owner"])
        account.acc_number = data["acc_number"]
        account._balance = data["balance"]
        account.is_blocked = data["is_blocked"]
        return account



    def __str__(self):
        return f"{self.acc_number} | {self.owner} | {self.balance:.2f} грн"

    def __repr__(self):
        return f"Account('{self.acc_number}', {self.balance:.2f})"

    def __eq__(self, other):
        return isinstance(other, Account) and self.acc_number == other.acc_number

    def __lt__(self, other):
        return isinstance(other, Account) and self.balance < other.balance



class SavingsAccount(Account):

    def __init__(self, owner:str, balance:float = 0, rate: int = 5):
        super().__init__(owner, balance)
        self.rate = rate

    @property
    def kind(self):
        return "Ощадний"

    def add_interest(self):
        interest = round(self._balance * self.rate / 100)
        self._balance += interest
        return interest

    def to_dict(self):
        data = super().to_dict()
        data["rate"] = self.rate
        return data

    @classmethod
    def from_dict(cls, data):
        account = super().from_dict(data)
        account.rate = data["rate"]
        return account




class CreditAccount(Account):
    def __init__(self, owner:str, balance:float = 0, limit: float = 10000):
        super().__init__(owner, balance)
        self.limit = limit

    @property
    def kind(self):
        return "Кредитний"

    @property
    def available(self):
        return round(self._balance + self.limit, 2)

    def to_dict(self):
        data = super().to_dict()
        data["limit"] = self.limit
        return data

    @classmethod
    def from_dict(cls, data):
        account = super().from_dict(data)
        account.limit = data["limit"]
        return account

