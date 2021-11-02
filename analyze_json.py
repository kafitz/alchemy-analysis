#!/usr/bin/env python
import json
from pprint import pprint

DIVISORS = {
    'USDC': 1E6,
    'CADC': 1E18,
}


# iterate over json file and generate a list of deposit transactions
def process_deposits(currency_pair, request_id):
    cache_fp = f'{currency_pair}-deposits-{request_id}.json'
    with open(cache_fp, 'r') as cache_f:
        data = json.load(cache_f)

    deposits = []
    for transfer in data['result']['transfers']:
        value = int(transfer['rawContract']['value'], 16) / DIVISORS[transfer['asset']]
        deposits.append(
            (transfer['from'], transfer['blockNum'], transfer['asset'], value)
        )
    return deposits


# iterate over json file and generate a list of withdrawal transactions
def process_withdrawals(currency_pair, request_id):
    cache_fp = f'{currency_pair}-withdrawals-{request_id}.json'
    with open(cache_fp, 'r') as cache_f:
        data = json.load(cache_f)

    withdrawals = []
    for transfer in data['result']['transfers']:
        value = int(transfer['rawContract']['value'], 16) / DIVISORS[transfer['asset']]
        withdrawals.append(
            (transfer['to'], transfer['blockNum'], transfer['asset'], value)
        )
    return withdrawals


# sum list of formatted transfers
def total(transfers):
    balance = {}
    for _, _, asset, value in transfers:
        balance.setdefault(asset, 0)
        if value:
            balance[asset] += float(value)
    return balance


if __name__ == '__main__':
    ## TRYB / USDC
    ## 
    # deposits = process_deposits('TRYB-USDC', request_id=0)
    # withdrawals = process_withdrawals('TRYB-USDC', request_id=0)

    # total_deposits = total(deposits)
    # print('deposits:')
    # print(total_deposits)

    # total_withdrawals = total(withdrawals)
    # print('withdrawals:')
    # print(total_withdrawals)

    # print('net (USDC):', total_deposits['USDC'] - total_withdrawals['USDC'])
    # print('net (TRYB):', total_deposits['TRYB'] - total_withdrawals['TRYB'])

    ## CADC / USDC
    ## 
    deposits = process_deposits('CADC-USDC', request_id=0)
    withdrawals = process_withdrawals('CADC-USDC', request_id=0)

    total_deposits = total(deposits)
    print('deposits:')
    print(total_deposits)

    total_withdrawals = total(withdrawals)
    print('withdrawals:')
    print(total_withdrawals)

    print('net (USDC):', total_deposits['USDC'] - total_withdrawals['USDC'])
    print('net (CADC):', total_deposits['CADC'] - total_withdrawals['CADC'])


