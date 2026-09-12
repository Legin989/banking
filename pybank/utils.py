from functools import wraps
from pybank.exceptions import BankError

def log_operation(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
        except BankError as e:
            print(f"[LOG] {func.__name__} -> {type(e).__name__}")
        else:
            print(f"[LOG] {func.__name__} -> OK")
            return result

    return wrapper