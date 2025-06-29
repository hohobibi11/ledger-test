from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class Transaction:
  id: str
  amount: Decimal
  balance: Decimal
  currency: str
  source_tx_id: Optional[str] = None
