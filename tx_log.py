import threading
from collections import defaultdict
from decimal import Decimal
from typing import List, Iterator

from transaction import Transaction


class TxLog:
    def __init__(self):
        # could use a dic for better performance
        # but this simulates best the db/orm behavior
        self._log: List[Transaction] = []
        self._lock = threading.Lock()
        # denormalization for performance
        self._balance = defaultdict(lambda: Decimal('0'))

    def append(self, item: Transaction):
        with self._lock:
            self._log.append(item)
            self._balance[item.currency] += item.balance

    def items(self):
        with self._lock:
            return list(self._log)

    def item(self, tx_id: str) -> Transaction:
        with self._lock:
            tx = next((t for t in self._log if t.id == tx_id), None)
            if tx is None:
                raise ValueError("Transaction not found")

        return tx

    def consume(self, tx_id: str, amount: Decimal):
        tx = self.item(tx_id)
        if tx.amount < amount:
            raise ValueError("Insufficient funds")

        with self._lock:
            tx.balance -= amount
            self._balance[tx.currency] -= amount

    def balance(self):
        with self._lock:
            result = self._balance
        return result

    def currencies(self):
        with self._lock:
            result = self._balance.keys()
        return result

    def __len__(self):
        with self._lock:
            return len(self._log)

    def __iter__(self) -> Iterator[Transaction]:
        with self._lock:
            snapshot = list(self._log)
        return iter(snapshot)
