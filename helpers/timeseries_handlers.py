#!/usr/bin/env python
import json


def generate_timeseries(cur1, cur2, liquidity_txs, zap_txs):
    cur1_series = []
    cur2_series = []
    for tx in liquidity_txs:
        val1 = float(tx['val1'])
        if tx['type'] in ['withdrawal', 'zap-withdrawal']:
            val1 *= -1
        cur1_series.append([tx['blockNum'], val1, None])

        is_zap = tx['type'] in ['zap-deposit', 'zap-withdrawal']
        if not is_zap:
            val2 = float(tx['val2'])
            if tx['type'] in ['withdrawal']:
                val2 *= -1
            cur2_series.append([tx['blockNum'], val1, None])

    for tx, txs in zap_txs.items():
        print(txs)
        import sys; sys.exit()


    cur1_total = 0
    cur2_total = 0
    # for tx in cur1_series:
    #     if tx['type'] == 'deposit':
    #         cur1_total += val1
    #         cur2_total += val2
    #     elif tx['type'] == 'withdrawal':
    #         cur1_total -= val1
    #         cur2_total -= val2

    series = {
        'cur1': {
            'name': cur1,
            'series': sorted(cur1_series, key=lambda d: d[0])
        },
        'cur2': {
            'name': cur2,
            'series': sorted(cur2_series, key=lambda d: d[0])
        }
    }
    with open(f'./outputs/{cur1.lower()}-{cur2.lower()}-net_positions.json', 'w') as data_f:
        json.dump(series, data_f, indent=4)
