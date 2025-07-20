from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class Transaction:
    id: str
    amount: Decimal
    balance: Decimal
    fee: Decimal
    currency: str
    source_tx_id: Optional[str] = None
    conversion_rate: Decimal = Decimal('1')

    @property
    def initial_balance(self) -> Decimal:
        return self.amount - self.fee
