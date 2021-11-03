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


def format_transfers(json_data, deposit=False, withdrawal=False):
    transfers = []
    for transfer in json_data['result']['transfers']:
        asset = _get_asset(transfer)
        value = int(transfer['rawContract']['value'], 16) / DIVISORS[asset]
        if deposit:
            transfers.append(
                (transfer['from'], transfer['to'], int(transfer['blockNum'], 16), transfer['hash'], asset, value)
            )
        elif withdrawal:
            transfers.append(
                (transfer['to'], transfer['from'], int(transfer['blockNum'], 16), transfer['hash'], asset, value)
            )
        else:
            raise Exception('Cached data type not specified.')            
    return transfers


def format_zap_transfers(json_data, deposit=False, withdrawal=False):
    transfers = []
    for transfer in json_data['result']['transfers']:
        asset = _get_asset(transfer)
        value = int(transfer['rawContract']['value'], 16) / DIVISORS[asset]
        if deposit:
            transfers.append(
                (transfer['from'], transfer['to'], int(transfer['blockNum'], 16), transfer['hash'], asset, value)
            )
        elif withdrawal:
            transfers.append(
                (transfer['to'], transfer['from'], int(transfer['blockNum'], 16), transfer['hash'], asset, value)
            )
        else:
            raise Exception('Cached data type not specified.')            
    return transfers


def filter_zap_txs(hash_txs, zap_hashes):
    for hash in zap_hashes:
        hash_txs.pop(hash, None)
    return hash_txs