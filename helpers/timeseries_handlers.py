#!/usr/bin/env python
import json


def generate_timeseries(cur1, cur2, liquidity_txs, swap_txs):
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
            cur2_series.append([tx['blockNum'], val2, None])

    for tx in swap_txs:
        val1 = float(tx['val1'])
        val2 = float(tx['val2'])
        if tx['cur1'] == cur1:
            cur1_series.append([tx['blockNum'], val1, None])
            cur2_series.append([tx['blockNum'], -val2, None])
        elif tx['cur1'] == cur2:
            cur1_series.append([tx['blockNum'], -val1, None])
            cur2_series.append([tx['blockNum'], val2, None])            

    cur1_total = 0
    merged_cur1_series = sorted(cur1_series, key=lambda d: d[0])
    for tx in merged_cur1_series:
        cur1_total += tx[1]
        tx[2] = cur1_total

    cur2_total = 0
    merged_cur2_series = sorted(cur2_series, key=lambda d: d[0])
    for tx in merged_cur2_series:
        cur2_total += tx[1]
        tx[2] = cur2_total

    # for tx in merged_cur1_series:
    #     print(tx)

    # print()
    # for tx in merged_cur2_series:
    #     print(tx)        

    # print(cur1_total, cur2_total)
    # print(len(merged_cur1_series))

    series = {
        'cur1': {
            'name': cur1,
            'series': merged_cur1_series,
        },
        'cur2': {
            'name': cur2,
            'series': merged_cur2_series,
        }
    }
    with open(f'./outputs/{cur1.lower()}-{cur2.lower()}-net_positions.json', 'w') as data_f:
        json.dump(series, data_f, indent=4)
