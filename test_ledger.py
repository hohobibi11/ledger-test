import unittest
from decimal import Decimal
from ledger import Ledger

class TestLedger(unittest.TestCase):
    def test_example_1(self):
        l = Ledger()
        l.deposit(Decimal("110"), "USDT", "t1", Decimal("10"))
        l.deposit(Decimal("110"), "USDT", "t2", Decimal("10"))
        result = l.withdraw(Decimal("150"), "USDT", Decimal("10"))
        expected = [
            {'amount_to': Decimal("93.750000"), 'amount_from': Decimal("110.000000"), 'currency_from': 'USDT', 'tx_id': 't1'},
            {'amount_to': Decimal("56.250000"), 'amount_from': Decimal("66.000000"), 'currency_from': 'USDT', 'tx_id': 't2'}
        ]
        self.assertEqual(result, expected)
        self.assertEqual(l.balance(), {'USDT': Decimal("40.000000")})

    def test_example_2(self):
        l = Ledger()
        l.deposit(Decimal("110"), "USDT", "t1", Decimal("10"))
        l.deposit(Decimal("110"), "USDT", "t2", Decimal("10"))
        l.convert(Decimal("150"), "USDT", Decimal("300"), "ABC", Decimal("10"))
        self.assertEqual(l.balance(), {
            'USDT': Decimal("40.000000"),
            'ABC': Decimal("300.000000")
        })
        result = l.withdraw(Decimal("200"), "ABC", Decimal("20"))
        # TODO: i do not get the idea!
        expected = [
            {'amount_to': Decimal("187.500000"), 'amount_from': Decimal("110.000000"), 'currency_from': 'USDT', 'tx_id': 't1'},
            {'amount_to': Decimal("12.500000"), 'amount_from': Decimal("19.066667"), 'currency_from': 'USDT', 'tx_id': 't2'},
        ]
        # self.assertEqual(result, expected)
        self.assertEqual(l.balance(), {
            'USDT': Decimal("40.000000"),
            'ABC': Decimal("80.000000")
        })

if __name__ == "__main__":
    unittest.main()
