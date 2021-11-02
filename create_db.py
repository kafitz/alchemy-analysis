#!/usr/bin/env python
import dotenv
import json
import requests
import os
import time

dotenv.load_dotenv()

ALCHEMY_API_KEY = os.environ.get('ALCHEMY_API_KEY')
ALCHEMY_BASE_URL = f'https://eth-mainnet.alchemyapi.io/v2/{ALCHEMY_API_KEY}'


POOL_CONTRACTS = {
    'CADC-USDC': ('0xa6C0CbCaebd93AD3C6c94412EC06aaA37870216d', 12459301),
    'EURS-USDC': ('0x1a4Ffe0DCbDB4d551cfcA61A5626aFD190731347', 12459337),
    'XSGD-USDC': ('0x2baB29a12a9527a179Da88F422cDaaA223A90bD5', 12459348),
    'NZDS-USDC': ('0xe9669516e09f5710023566458f329cce6437aaac', 13283851),
    'TRYB-USDC': ('0xc574a613a3900e4314da13eb2287f13689a5b64d', 13234461),
}
STAKING_CONTRACTS = {
    'CADC-USDC': ('0x84Bf8151394dcF32146965753B28760550f3D7A8', 12459404),
    'EURS-USDC': ('0x5EaAEff69f2aB64d1CC0244FB31B236cA989544f', 12459411),
    'XSGD-USDC': ('0xd52D48Db08e8224ef6E2be8F54f3c84e790b1c32', 12459420),
    'NZDS-USDC': ('0xe06FA52e0d2D58Fe192285bfa0507F09cDd9824a', 13232886),
    'TRYB-USDC': ('0xdDB720069fdfE7BE2E2883A1c06BE0f353f7C4c8', 13282257),
}


def get_gas_price():
    params = {
        'jsonrpc': '2.0',
        'method': 'eth_gasPrice',
        'id': 1,
        'params': []
    }
    r = requests.post(ALCHEMY_BASE_URL, json=params)
    print(r)
    print(r.json())



def get_asset_transfers(currency_pair, contract_address, start_block, request_id=0, deposits=True):
    label = 'deposits' if deposits else 'withdrawals'
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
        if deposits:
            params['params'][0]['toAddress'] = contract_address
        else:
            params['params'][0]['fromAddress'] = contract_address


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


def _get_or_init_request_idx(currency_pair, tx_type):
    new_idx = 0
    for fn in sorted(os.listdir()):
        if currency_pair in fn:
            base_fn_parts = fn.rstrip('.json').split('-')
            if base_fn_parts[2] != tx_type:
                continue
            new_idx = int(base_fn_parts[-1]) + 1
    return new_idx

def _get_next_block_num(transfers):
    return int(transfers[-1]['blockNum'], 16) + 1


def _load_next_block_from_file(currency_pair, tx_type, request_id):
    cache_fp = f'{currency_pair}-{tx_type}-{request_id}.json'
    with open(cache_fp, 'r') as cache_f:
        data = json.load(cache_f)
    next_block = _get_next_block_num(data['result']['transfers'])
    return next_block


# run fetch request in loop based upon latest block number until no new transactions exist
def fetch_all_data(currency_pair, contract_info, deposits=True):
    contract_address, start_block = contract_info
    tx_type = 'deposits' if deposits is True else 'withdrawals'
    
    print(f'Fetching {tx_type} for {currency_pair}...')

    # initialize request id and start block from 0 or from existing data
    request_idx = _get_or_init_request_idx(currency_pair, tx_type)
    if request_idx != 0:
        start_block = _load_next_block_from_file(currency_pair, tx_type, request_idx - 1)

    first_request = True
    transfers_data = None
    while True:
        # sleep between consecutive requests and get next start block
        # from last seen block num + 1
        if not first_request:
            time.sleep(1)
            start_block = _get_next_block_num(transfers_data)

        # perform API requests and break when new data is empty
        print('Start block num:', start_block)
        data = get_asset_transfers(
            currency_pair,
            contract_address, 
            start_block, 
            request_idx,
            deposits=deposits)
        if 'result' not in data or len(data['result']['transfers']) == 0:
            break
        transfers_data = data['result']['transfers']
        print('Results:', len(transfers_data))
        request_idx += 1
        first_request = False


if __name__ == '__main__':
    for currency_pair, contract_info in POOL_CONTRACTS.items():
        fetch_all_data(currency_pair, contract_info, deposits=True)
        fetch_all_data(currency_pair, contract_info, deposits=False)
        # break
