class BankError(Exception):
    """Кореневий виняток PyBank"""

class AccountError(BankError):
    ...

class OperationError(BankError):
    ...

class StorageError(BankError):
    ...

class AccountNotFound(AccountError):
    def __init__(self, acc_number):
        super().__init__(f"Акаунт {acc_number} не знайдено")


class AccountBlocked(AccountError):
    def __init__(self, acc_number):
        super().__init__(f"Акаунт {acc_number} заблоковано")

class InvalidAmount(OperationError):
    def __init__(self, amount):
        super().__init__(f"некоректна сума: {amount!r} грн")

class InsufficientFunds(OperationError):
    def __init__(self, acc_number, available, required):
        super().__init__(
            f"на {acc_number} бракує {required - available:.2f} грн "
            f"(доступно {available:.2f} грн, потрібно {required} грн)"
        )

class LimitExceeded(OperationError):
    def __init__(self, amount, limit):
        super().__init__(f"Переказ на суму {amount} грн перевищує ліміт {limit} грн")