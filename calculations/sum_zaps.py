#!/usr/bin/env python

from constants import BLACKHOLE_ADDRESS, POOL_CONTRACTS, ZAP_CONTRACT_INFO


def calculate_sum_zap_txs(cur1, cur2, hash_txs, hash_txs_lookup):
    totals = {
        cur1: 0,
        cur2: 0,
    }
    for tx_hash, txs in hash_txs.items():
        if not (cur1 in hash_txs_lookup[tx_hash] and cur2 in hash_txs_lookup[tx_hash]):
            continue

        num = 0
        for tx in txs:
            ignore_pools = [info[0].lower() for _, info in POOL_CONTRACTS.items()]
            ignore_contracts = [ZAP_CONTRACT_INFO[0].lower(), BLACKHOLE_ADDRESS]

            ignore_tx = False
            if tx['toAddress'].lower() in ignore_pools and tx['fromAddress'].lower() in ignore_contracts:
                ignore_tx = True
            if tx['fromAddress'].lower() in ignore_pools and tx['toAddress'].lower() in ignore_contracts:
                ignore_tx = True
            if ignore_tx:
                continue
            num += 1

            if tx['asset'] == cur1:
                if tx['type'] in ['deposit', 'zap-deposit']:
                    totals[cur1] += tx['value']
                elif tx['type'] in ['withdrawal', 'zap-withdrawal']:
                    totals[cur1] -= tx['value']
            elif tx['asset'] == cur2:
                if tx['type'] in ['deposit', 'zap-deposit']:
                    totals[cur2] += tx['value']
                elif tx['type'] in ['withdrawal', 'zap-withdrawal']:
                    totals[cur2] -= tx['value'] 
    return totals
