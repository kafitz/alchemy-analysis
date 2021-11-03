#!/usr/bin/env python

def calculate_net_balances(swap_txs, currencies, net_liquidity_cur1, net_liquidity_cur2, net_zaps):
    currency1, currency2 = currencies
    chg_cur1, chg_cur2 = 0, 0
    for tx in swap_txs:
        if tx['cur1'] == currency1:
            chg_cur1 -= tx['val1']
            chg_cur2 += tx['val2']
        elif tx['cur1'] == currency2:
            chg_cur2 -= tx['val1']
            chg_cur1 += tx['val2']

    print(f'balance ({currency1}):', net_liquidity_cur1 - chg_cur1 + net_zaps[currency1])
    print(f'balance ({currency2}):', net_liquidity_cur2 - chg_cur2 + net_zaps[currency2])
