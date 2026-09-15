import json
from .accounts import Account,CreditAccount, SavingsAccount
from .exceptions import StorageError

ACCOUNT_TYPES = {
    "Account": Account,
    "SavingsAccount": SavingsAccount,
    "CreditAccount": CreditAccount,
}


def save_bank(bank, path):
    data = {
        "name": bank.name,
        "accounts": [account.to_dict() for account in bank],
    }
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    return len(data["accounts"])


def load_accounts(path):
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as error:
        raise StorageError(f"файл {path} не знайдено") from error
    except json.JSONDecodeError as error:
        raise StorageError(f"файл {path} пошкоджено") from error

    accounts = []
    for item in data["accounts"]:
        account_class = ACCOUNT_TYPES[item["type"]]
        accounts.append(account_class.from_dict(item))
    return accounts
