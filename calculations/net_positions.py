#!/usr/bin/env python
import json


# sum list of formatted transfers
# [(address, blockNum, hash, asset, value), ...]
def total(transfers):
    balance = {}
    for t in transfers:
        asset = t['asset']
        value = t['value']
        balance.setdefault(asset, 0)
        if value:
            balance[asset] += float(value)
    return balance

# calculate current net positions of all transactions regardless of type
def calculate_net_positions(deposits, withdrawals, currencies):
    cur1, cur2 = currencies
    total_deposits = total(deposits)
    total_withdrawals = total(withdrawals)

    print('deposits:')
    print(total_deposits)
    print('withdrawals:')
    print(total_withdrawals)
    print()
    print(f'net ({cur1}):', total_deposits[cur1] - total_withdrawals[cur1])
    print(f'net ({cur2}):', total_deposits[cur2] - total_withdrawals[cur2])
