from pybank import (
    Account,
    CreditAccount,
    SavingsAccount,
    Bank,
    BankError,
    load_accounts,
    save_bank
)

FILE_NAME = "bank.json"

MENU = """
1 - Відкрити рахунок
2 - Показати рахунки
3 - Поповнити 
4 - Зняти 
5 - Переказ
6 - Нарахувати відсотокк
7 - Журнал операцій
8 - Зберегти у файл
9 - Завантажити з файлу
0 - Вихід
"""


def ask_amount(prompt):
    while True:
        text = input(prompt).strip()
        try:
            return float(text)
        except ValueError:
            print("Введіть число, наприклад 150 або 99.50")


def ask_number(prompt):
    return input(prompt).strip().upper()


def open_account(bank):
    print("Тип рахунку: 1 - базовийб 2 - ощаднийб 3 - кредитний")
    kind = input("Тип: ").strip()
    if kind not in ("1", "2", "3"):
        print("невідомий тип рахунку")
        return
    owner = input("Власник: ").strip()
    balance = ask_amount("Початковий баланс: ")

    if kind == "1":
        account = Account(owner, balance)
    elif kind == "2":
        rate = ask_amount("Річна ставка %: ")
        account = SavingsAccount(owner, balance, rate=int(rate))
    else:
        limit = ask_amount("Кредитний ліміт: ")
        account = CreditAccount(owner, balance, limit=limit)

    bank.open_account(account)
    print(f"Відкрито: {account}")


def show_account(bank):
    if len(bank) == 0:
        print("Рахунків ще немає")
        return

    for account in bank:
        print(f" {account}")
    print(f"Разом: {bank.total:.2f} грн")


def deposit(bank):
    acc_number = ask_number("Номер рахунку: ")
    amount = ask_amount("Сума: ")
    new_balance = bank.deposit(acc_number, amount)
    print(f"Баланс {acc_number}: {new_balance:.2f} грн")


def withdraw(bank):
    acc_number = ask_number("Номер рахунку: ")
    amount = ask_amount("Сума: ")
    new_balance = bank.withdraw(acc_number, amount)
    print(f"Баланс {acc_number}: {new_balance} грн")


def transfer(bank):
    source = ask_number("З рахунку: ")
    target = ask_number("На рахунок: ")
    amount = ask_amount("Сума: ")
    bank.transfer(source, target, amount)
    print(f"Переказано {amount:.2f} грн {source} -> {target}")

def add_interest(bank):
    acc_number = ask_number("Номер ощадного рахунку: ")
    account = bank[acc_number]
    if not isinstance(account, SavingsAccount):
        print(f"{acc_number} - не ощадний рахунок")
        return

    interest = account.add_interest()
    print(f"Нараховано {interest:.2f} грн, баланс: {account.balance:.2f}  грн")



def show_log(bank):
    if len(bank.log) == 0:
        print("Журнал порожній")
        return
    for record in bank.log:
        print(f" {record}")


def save(bank):
    count = save_bank(bank, FILE_NAME)
    print(f"Збережено рахунків: {count} (файл {FILE_NAME})")


def load():
    accounts = load_accounts(FILE_NAME)
    bank = Bank("PyBank")
    for account in accounts:
        bank.open_account(account)
    print(f"Завантажено рахунків: {len(bank)}")
    return bank


def main():
    print("== PyBank ==")
    bank = Bank("PyBank")

    while True:
        print(MENU)
        choise = input("Ваш вибір: ").strip()

        try:
            if choise == "1":
                open_account(bank)
            elif choise == "2":
                show_account(bank)
            elif choise == "3":
                deposit(bank)
            elif choise == "4":
                withdraw(bank)
            elif choise == "5":
                transfer(bank)
            elif choise == "6":
                add_interest(bank)
            elif choise == "7":
                show_log(bank)
            elif choise == "8":
                save(bank)
            elif choise == "9":
                bank = load()
            elif choise == "0":
                print("До побачення!")
                break
            else:
                print("Немає такого пункту меню")
        except BankError as e:
            print(f"Помилка: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nДо побачення!")