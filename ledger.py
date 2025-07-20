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
            fee=fee,
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

            source_tx = self._transactions.item(tx.source_tx_id) if tx.source_tx_id is not None else tx
            tx_amount_from = (take * tx.amount / tx.initial_balance) / tx.conversion_rate
            source_amount_from = tx_amount_from if tx.source_tx_id is None else tx_amount_from * source_tx.amount / source_tx.initial_balance
            result.append({
                'amount_to': _round(amount * proportion),
                'amount_from': _round(source_amount_from),
                'currency_from': source_tx.currency,
                'tx_id': source_tx.id,
                'fee': _round(fee * proportion),
            })

            self._transactions.consume(tx.id, take)
            remaining -= take

        return result

    def withdraw(self, amount: Decimal, currency: str, fee: Decimal):
        return [{k: v for k, v in d.items() if k != 'fee'} for d in self._consume_funds(currency, amount, fee)]

    def convert(self, amount_from: Decimal, currency_from: str, amount_to: Decimal, currency_to: str, fee: Decimal):
        conversion_trace = self._consume_funds(currency_from, amount_from, fee)
        rate = amount_to / amount_from
        for record in conversion_trace:
            record_fee = record['fee'] * rate
            record_amount = record['amount_to'] * rate
            self._transactions.append(
                Transaction(
                    id=generate_random_tx_id(),
                    balance=record_amount,
                    amount=record_amount + record_fee,
                    fee=record_fee,
                    currency=currency_to,
                    source_tx_id=record['tx_id'],
                    conversion_rate=rate
                ))
