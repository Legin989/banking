from typing import Any


class Transaction:
    _counter = 0

    def __init__(self,kind, amount, source, target="-"):
        Transaction._counter += 1
        self.id = f"T{Transaction._counter:03d}"
        self.kind = kind
        self.amount = amount
        self.source = source
        self.target = target

    @classmethod
    def reset_counter(cls):
        Transaction._counter = 0

    def __str__(self):
        return f"{self.id} {self.kind}: {self.amount:.2f} грн ({self.source}) -> {self.target}"

    def __repr__(self):
        return f"Transaction(id={self.id}, kind={self.kind}, amount={self.amount}"



class LogIterator:
    def __init__(self, transactions):
        self._transactions = transactions
        self._position = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._position >= len(self._transactions):
            raise StopIteration
        transaction = self._transactions[self._position]
        self._position += 1
        return transaction

class TransactionLog:
    def __init__(self):
        self._transactions: list[Transaction] = []

    @property
    def total_amount(self):
        return round(sum(t.amount for t in self._transactions), 2)

    def by_kind(self, kind):
        for transaction in self._transactions:
            if transaction.kind == kind:
                yield transaction


    def add(self, transaction):
        self._transactions.append(transaction)
        return transaction

    def __iter__(self):
        return LogIterator(self._transactions)

    def __len__(self):
        return len(self._transactions)

    def __getitem__(self, index):
        return self._transactions[index]