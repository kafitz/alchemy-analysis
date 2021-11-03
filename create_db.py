#!/usr/bin/env python
import json
import requests
import os
import time

from config import ALCHEMY_BASE_URL
from constants import POOL_CONTRACTS, ZAP_CONTRACTS
from helpers import data_handlers, file_handlers


def get_asset_transfers(currency_pair, contract_address, start_block, label, request_id=0):
    cache_fp = f'{currency_pair}-{label}-{request_id}.json'
    if not os.path.exists(cache_fp):
        params = {
            'jsonrpc': '2.0',
            'method': 'alchemy_getAssetTransfers',
            'id': request_id,
            'params': [{
                'fromBlock': hex(start_block),
                'maxCount': hex(1000),
                'excludeZeroValue': True,
                'category': [
                    'external',
                    'token',
                ]
            }]
        }
        if label in ['deposits', 'zap-deposits']:
            params['params'][0]['toAddress'] = contract_address
        elif label in ['withdrawals', 'zap-withdrawals']:
            params['params'][0]['fromAddress'] = contract_address
        else:
            raise Exception(f'Label {label} not recognized. (deposits, zap-deposits, withdrawals, zap-withdrawals)')


        r = requests.post(ALCHEMY_BASE_URL, json=params)
        data = r.json()

        # only cache when data exists
        if 'result' in data and len(data['result']['transfers']) != 0:
            with open(cache_fp, 'w') as cache_f:
                json.dump(r.json(), cache_f)
    else:
        with open(cache_fp, 'r') as cache_f:
            data = json.load(cache_f)
    return data


# run fetch request in loop based upon latest block number until no new transactions exist
def fetch_all_data(currency_pair, contract_info, tx_type):
    print(f'Fetching {tx_type} for {currency_pair}...')
    contract_address, start_block = contract_info    

    # initialize request id and start block from 0 or from existing data
    request_idx = file_handlers.get_or_init_request_idx(currency_pair, tx_type)
    if request_idx != 0:
        start_block = file_handlers.load_next_block(currency_pair, tx_type, request_idx - 1)

    first_request = True
    while True:
        # sleep between consecutive requests and get next start block
        # from last seen block num + 1
        if not first_request:
            time.sleep(1)
            start_block = data_handlers.get_next_block_num(transfers_data)

        # perform API requests and break when new data is empty
        print('Start block num:', start_block)
        data = get_asset_transfers(
            currency_pair,
            contract_address, 
            start_block, 
            tx_type,
            request_idx)
        if 'result' not in data or len(data['result']['transfers']) == 0:
            break
        transfers_data = data['result']['transfers']
        print('Results:', len(transfers_data))
        request_idx += 1
        first_request = False


if __name__ == '__main__':
    for currency_pair, contract_info in POOL_CONTRACTS.items():
        if currency_pair != 'TRYB-USDC':
            continue

        fetch_all_data(currency_pair, contract_info, 'deposits')
        fetch_all_data(currency_pair, contract_info, 'withdrawals')

        # (zap_contract_address, pool_contract_start_blocks)
        zap_contract_info = (ZAP_CONTRACTS[currency_pair], contract_info[1])
        fetch_all_data(currency_pair, zap_contract_info, 'zap-deposits')
        fetch_all_data(currency_pair, zap_contract_info, 'zap-withdrawals')
        break

