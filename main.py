from decimal import Decimal

from ledger import Ledger


def main():
    l = Ledger()
    l.deposit(Decimal('110'), 'USDT', 't1', Decimal('10'))
    l.deposit(Decimal('110'), 'USDT', 't2', Decimal('10'))
    result = l.withdraw(Decimal('150'), 'USDT', Decimal('10'))
    print(result)
    print(l.balance())

    print('-------------------------------')

    l = Ledger()
    l.deposit(Decimal('110'), 'USDT', 't1', Decimal('10'))
    l.deposit(Decimal('110'), 'USDT', 't2', Decimal('10'))
    l.convert(Decimal('150'), 'USDT', Decimal('300'), 'ABC', Decimal('10'))
    print(l.balance())
    result = l.withdraw(Decimal('200'), 'ABC', Decimal('20'))
    print(result)
    print(l.balance())

if __name__ == '__main__':
    main()
