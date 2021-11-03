#!/usr/bin/env python


# sum list of formatted transfers
# [(address, blockNum, hash, asset, value), ...]
def total(transfers):
    balance = {}
    for _, _, _, asset, value in transfers:
        balance.setdefault(asset, 0)
        if value:
            balance[asset] += float(value)
    return balance


# calculate current net positions of all transactions regardless of type
def calculate_net_positions(deposits, withdrawals, currencies):
    total_deposits = total(deposits)
    total_withdrawals = total(withdrawals)
    
    currency1, currency2 = currencies
    print('deposits:')
    print(total_deposits)
    print('withdrawals:')
    print(total_withdrawals)
    print()
    print(f'net ({currency1}):', total_deposits[currency1] - total_withdrawals[currency1])
    print(f'net ({currency2}):', total_deposits[currency2] - total_withdrawals[currency2])
