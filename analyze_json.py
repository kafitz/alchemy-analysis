#!/usr/bin/env python
from pprint import pprint

from constants import CURRENCIES
from calculations.net_positions import calculate_net_positions
from calculations.net_liquidity_deposits import calculate_net_liquidity_deposits
from calculations.net_balances import calculate_net_balances
from calculations.sum_zaps import calculate_sum_zap_txs
from helpers import data_handlers, file_handlers, timeseries_handlers



# group transactions that have the same transaction hash
def group_single_transactions(deposits, withdrawals):
    hash_transactions = {}
    for d in deposits:
        d['type'] = 'deposit'
        hash_transactions.setdefault(d['hash'], []).append(d)
    for w in withdrawals:
        w['type'] = 'withdrawal'
        hash_transactions.setdefault(w['hash'], []).append(w)
    return hash_transactions


def create_zap_currency_lookup(hash_txs):
    valid = ['CADC', 'EURS', 'NZDS', 'TRYB', 'XSGD']
    lookup = {}
    for hash_tx, txs in hash_txs.items():
        for tx in txs:
            if tx['asset'] in valid:
                lookup[hash_tx] = (tx['asset'], 'USDC')
    return lookup


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
                'blockNum': txs[0]['blockNum'],
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
            zap_is_deposit = _grouped_tx_is_deposit(txs)
            target_asset = _zap_originator_destination_asset(txs, currencies, zap_is_deposit)

            # get total tx amount and append labeled transaction
            value = _tally_zap(txs, target_asset, zap_is_deposit)
            liquidity_txs.append({
                'blockNum': txs[0]['blockNum'],
                'type': 'zap-deposit' if zap_is_deposit else 'zap-withdrawal',
                'cur1': target_asset,
                'val1': value,
            })
        else:
            raise Exception(f"Unhandled number of transactions in group. (blockNum: {txs[0]['blockNum']}, hash: {tx_hash})")
    return liquidity_txs, swap_txs
    

# def group_zap_transactions(zap_hash_transactions):
#     zap_txs = []
#     sorted_hash_txs = sorted(zap_hash_transactions.items(), key=lambda d: d[1][0]['blockNum'])    
#     return zap_txs

def run(cur1, cur2):
    zap_deposits = file_handlers.load_cached_zap_data(deposit=True)
    zap_withdrawals = file_handlers.load_cached_zap_data(withdrawal=True)
    deposits = file_handlers.load_cached_data(cur1, cur2, deposit=True)
    withdrawals = file_handlers.load_cached_data(cur1, cur2, withdrawal=True)

    # create a lookup of hash -> (cur1, cur2) for each zap
    zap_hash_txs = group_single_transactions(zap_deposits, zap_withdrawals)
    lookup = create_zap_currency_lookup(zap_hash_txs)

    # group into liquidity transactions and trades
    currencies = [cur1, cur2]
    hash_txs = group_single_transactions(deposits, withdrawals)
    filtered_hash_txs = data_handlers.filter_zap_txs(hash_txs, zap_hash_txs.keys())
    liquidity_txs, swap_txs = sort_grouped_transactions(filtered_hash_txs, currencies)
    
    # # calculate sums
    calculate_net_positions(deposits, withdrawals, currencies)
    net_liquidity_cur1, net_liquidity_cur2 = calculate_net_liquidity_deposits(liquidity_txs, currencies)
    net_zap_txs = calculate_sum_zap_txs(cur1, cur2, zap_hash_txs, lookup)
    calculate_net_balances(swap_txs, currencies, net_liquidity_cur1, net_liquidity_cur2, net_zap_txs)

    # generate timeseries data for web charts
    # zap_txs = group_zap_transactions(zap_hash_txs)
    timeseries_handlers.generate_timeseries(cur1, cur2, liquidity_txs)



if __name__ == '__main__':
    ## CADC / USDC
    run(CURRENCIES.CADC, CURRENCIES.USDC)

    ## EURS / USDC
    run(CURRENCIES.EURS, CURRENCIES.USDC)    

    ## NZDS / USDC
    run(CURRENCIES.NZDS, CURRENCIES.USDC)

    ## TRYB / USDC
    run(CURRENCIES.TRYB, CURRENCIES.USDC)

    ## XSGD / USDC
    run(CURRENCIES.XSGD, CURRENCIES.USDC)    
