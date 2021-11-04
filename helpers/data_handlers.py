#!/usr/bin/env python
from constants import DIVISORS, TOKENS



def get_next_block_num(transfers):
    return int(transfers[-1]['blockNum'], 16) + 1


# fetch asset from transaction since it is not always returned (e.g., NZDS)
def _get_asset(transfer):
    asset = transfer['asset']
    if asset:
        return asset
    for name, address in TOKENS.items():
        if transfer['to'] == address:
            return name
        elif transfer['from'] == address:
            return name
        elif transfer['rawContract']['address'] == address:
            return name            


def format_transfers(json_data):
    transfers = []
    for t in json_data['result']['transfers']:
        asset = _get_asset(t)
        value = int(t['rawContract']['value'], 16) / DIVISORS[asset]
        transfers.append({
            'fromAddress': t['from'],
            'toAddress': t['to'],
            'blockNum': int(t['blockNum'], 16),
            'hash': t['hash'],
            'asset': asset,
            'value': value,
        })        
    return transfers


def filter_zap_txs(hash_txs, zap_hashes):
    for hash in zap_hashes:
        hash_txs.pop(hash, None)
    return hash_txs
