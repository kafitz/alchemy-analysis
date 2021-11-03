#!/usr/bin/env python
import json
from pprint import pprint

from calculations.net_positions import calculate_net_positions
from calculations.net_liquidity_deposits import calculate_net_liquidity_deposits
from calculations.net_balances import calculate_net_balances


class CURRENCIES:
    CADC = 'CADC'
    EURS = 'EURS'
    NZDS = 'NZDS'
    USDC = 'USDC'


DIVISORS = {
    'USDC': 1E6,
    'CADC': 1E18,
    'EURS': 1E2,
    'NZDS': 1E18,
}


# iterate over json file and generate a list of formatted transactions
def load_cached_data(cache_fp, deposit=False):
    with open(cache_fp, 'r') as cache_f:
        data = json.load(cache_f)

    transfers = []
    for transfer in data['result']['transfers']:
        # print(transfer, int(transfer['rawContract']['value'], 16) / DIVISORS[transfer['asset']])
        value = int(transfer['rawContract']['value'], 16) / DIVISORS[transfer['asset']]
        if deposit:
            transfers.append(
                (transfer['to'], int(transfer['blockNum'], 16), transfer['hash'], transfer['asset'], value)
            )
        else:
            transfers.append(
                (transfer['from'], int(transfer['blockNum'], 16), transfer['hash'], transfer['asset'], value)
            )            
    return transfers


# group transactions that have the same transaction hash
def group_single_transactions(deposits, withdrawals):
    hash_transactions = {}
    for address, block_num, tx_hash, asset, value in deposits:
        hash_transactions.setdefault(tx_hash, []).append({
            'blockNum': block_num,
            'toAddress': address,
            'asset': asset,
            'value': value,
            'type': 'deposit'
        })
    for address, block_num, tx_hash, asset, value in withdrawals:
        hash_transactions.setdefault(tx_hash, []).append({
            'blockNum': block_num,
            'fromAddress': address,
            'asset': asset,
            'value': value,
            'type': 'withdrawal'
        })
    return hash_transactions


# determine whether a zap transaction is a deposit or withdrawal depending
# on the greatest number of transaction types (naive inference)
def _grouped_tx_is_deposit(txs):
    deposits, withdrawals = 0, 0
    for tx in txs:    
        _type = tx['type']
        if _type == 'deposit':
            deposits += 1
        elif _type == 'withdrawal':
            withdrawals += 1
    # should never have equal number of deposits/withdrawals
    # in transaction if zap
    assert deposits != withdrawals
    return deposits > withdrawals


# determine the originator/destination asset by looking for the
# single transaction that doesn't match the others in its group
def _zap_originator_destination_asset(txs, currencies, is_deposit):
    def __filter_txs(txs, _type):
        filtered = [tx for tx in txs if tx['type'] == _type]
        assert len(filtered) == 1
        return filtered[0]

    cur1, cur2 = currencies
    if is_deposit:
        withdrawal_tx = __filter_txs(txs, 'withdrawal')
        return cur2 if withdrawal_tx['asset'] == cur1 else cur1
    else:
        deposit_tx = __filter_txs(txs, 'deposit')
        return cur2 if deposit_tx['asset'] == cur1 else cur1


# sum all txs that are grouped by hash that match the target originating (deposit)
# or desination (withdraw) asset
def _tally_zap(txs, target_asset, is_deposit):
    value = 0
    if is_deposit:
        for tx in txs:
            if tx['asset'] == target_asset and tx['type'] == 'deposit':
                value += tx['value']
    else:
        for tx in txs:
            if tx['asset'] == target_asset and tx['type'] == 'withdrawal':
                value += tx['value']
    return value


# sort transactions grouped by hash into `liquidity` or `swap` transactions
def sort_grouped_transactions(hash_transactions, currencies):
    liquidity_txs = []
    swap_txs = []
    # sort dictionary of lists of dictionaries by `blockNum` key
    # { tx_hash: [{blockNum: 123}, {blockNum: 123}]}
    sorted_hash_txs = sorted(hash_transactions.items(), key=lambda d: d[1][0]['blockNum'])
    for tx_hash, txs in sorted_hash_txs:
        if len(txs) == 2:
            new_tx = {
                'cur1': txs[0]['asset'],
                'val1': txs[0]['value'],
                'cur2': txs[1]['asset'],
                'val2': txs[1]['value'],
            }
            if all([tx['type'] == 'deposit' for tx in txs]):
                new_tx['type'] = 'deposit'
                liquidity_txs.append(new_tx)
            elif all([tx['type'] == 'withdrawal' for tx in txs]):
                new_tx['type'] = 'withdrawal'
                liquidity_txs.append(new_tx)
            else:
                # label as swap if both deposit and withdrawal exist
                new_tx['type'] = 'swap'
                swap_txs.append(new_tx)
        elif len(txs) == 4:
            is_deposit = _grouped_tx_is_deposit(txs)
            target_asset = _zap_originator_destination_asset(txs, currencies, is_deposit)

            # get total tx amount and append labeled transaction
            value = _tally_zap(txs, target_asset, is_deposit)
            liquidity_txs.append({
                'type': 'zap-deposit' if is_deposit else 'zap-withdrawal',
                'cur1': target_asset,
                'val1': value,
            })
        else:
            raise Exception(f"Unhandled number of transactions in group. (blockNum: {txs[0]['blockNum']}, hash: {tx_hash})")
    return liquidity_txs, swap_txs
    

def run(cur1, cur2):
    deposits = load_cached_data(f'{cur1}-{cur2}-deposits-0.json', deposit=True)
    withdrawals = load_cached_data(f'{cur1}-{cur2}-withdrawals-0.json')

    # group into liquidity transactions and trades
    currencies = [cur1, cur2]    
    hash_txs = group_single_transactions(deposits, withdrawals)
    liquidity_txs, swap_txs = sort_grouped_transactions(hash_txs, currencies)
    
    # calculate sums
    calculate_net_positions(deposits, withdrawals, currencies)
    net_liquidity_CADC, net_liquidity_USDC = calculate_net_liquidity_deposits(liquidity_txs, currencies)
    calculate_net_balances(swap_txs, currencies, net_liquidity_CADC, net_liquidity_USDC)


if __name__ == '__main__':
    # # CADC / USDC
    # run(CURRENCIES.CADC, CURRENCIES.USDC)

    # EURS / USDC
    run(CURRENCIES.EURS, CURRENCIES.USDC)    

    # # NZDS / USDC
    # run(CURRENCIES.NZDS, CURRENCIES.USDC)
