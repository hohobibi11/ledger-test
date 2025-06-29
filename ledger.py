import random
import string
from decimal import Decimal, getcontext, ROUND_HALF_UP

from transaction import Transaction
from tx_log import TxLog

getcontext().prec = 28


def _round(value):
    return value.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)


def generate_random_tx_id(length=16):
    characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    return ''.join(random.choices(characters, k=length))


class Ledger:
    def __init__(self):
        self._transactions = TxLog()

    def _check_currency(self, currency: str):
        if currency not in self._transactions.currencies():
            raise ValueError("No such currency")

    def deposit(self, amount: Decimal, currency: str, tx_id: str, fee: Decimal):
        net_amount = _round(amount - fee)
        if net_amount <= 0:
            raise ValueError("fee should not be greater then or equal amount")

        self._transactions.append(Transaction(
            id=tx_id,
            amount=amount,
            balance=net_amount,
            currency=currency
        ))

    def balance(self):
        return self._transactions.balance()

    def _consume_funds(self, currency, amount: Decimal, fee: Decimal):
        self._check_currency(currency)

        required_amount = amount + fee
        if self.balance()[currency] < required_amount:
            raise ValueError("Insufficient funds")

        result = []
        remaining = required_amount
        iterator = iter(self._transactions)

        while remaining > Decimal('0'):
            tx = next(iterator)
            if tx.currency != currency or tx.balance == 0:
                continue

            take = min(tx.balance, remaining)
            proportion = take / required_amount
            result.append({
                'amount_to': _round(amount * proportion),
                'amount_from': _round(take / tx.balance * tx.amount),
                'currency_from': currency,
                'tx_id': tx.source_tx_id if tx.source_tx_id is not None else tx.id,
            })

            self._transactions.consume(tx.id, take)
            remaining -= take

        return result

    def withdraw(self, amount: Decimal, currency: str, fee: Decimal):
        return self._consume_funds(currency, amount, fee)

    def convert(self, amount_from: Decimal, currency_from: str, amount_to: Decimal, currency_to: str, fee: Decimal):
        conversion_trace = self._consume_funds(currency_from, amount_from, fee)
        rate = amount_to / amount_from
        for record in conversion_trace:
            self._transactions.append(
                Transaction(
                    id=generate_random_tx_id(),
                    balance=record['amount_to'] * rate,
                    amount=record['amount_to'] * rate,
                    currency=currency_to,
                    source_tx_id=record['tx_id'],
                ))
