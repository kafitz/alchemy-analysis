#!/usr/bin/env python


def calculate_net_liquidity_deposits(liquidity_txs, currencies):
    liquidity_deposits = {}
    liquidity_withdrawals = {}
    for tx in liquidity_txs:
        if tx['type'] in ['deposit', 'zap-deposit']:
            cur1 = tx['cur1']
            liquidity_deposits.setdefault(cur1, 0)
            liquidity_deposits[cur1] += tx['val1']
            
            if tx['type'] == 'deposit':
                cur2 = tx['cur2']
                liquidity_deposits.setdefault(cur2, 0)
                liquidity_deposits[cur2] += tx['val2']
        
        elif tx['type'] in ['withdrawal', 'zap-withdrawal']:
            cur1 = tx['cur1']
            liquidity_withdrawals.setdefault(cur1, 0)
            liquidity_withdrawals[cur1] += tx['val1']

            if tx['type'] == 'withdrawal':
                cur2 = tx['cur2']
                liquidity_withdrawals.setdefault(cur2, 0)
                liquidity_withdrawals[cur2] += tx['val2']

        else:
            raise Exception(f"Unexpected tx type: {tx['type']}")

    currency1, currency2 = currencies
    net_liquidity_currency1 = liquidity_deposits[currency1] - liquidity_withdrawals[currency1]
    net_liquidity_currency2 = liquidity_deposits[currency2] - liquidity_withdrawals[currency2]

    print()
    print('liquidity deposits:')
    print(liquidity_deposits)
    print('liquidity withdrawals:')
    print(liquidity_withdrawals)
    print(f'net liquidity ({currency1}):', net_liquidity_currency1)
    print(f'net liquidity ({currency2}):', net_liquidity_currency2)
    return net_liquidity_currency1, net_liquidity_currency2
