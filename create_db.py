#!/usr/bin/env python
import dotenv
import json
import requests
import os

dotenv.load_dotenv()

ALCHEMY_API_KEY = os.environ.get('ALCHEMY_API_KEY')
ALCHEMY_BASE_URL = f'https://eth-mainnet.alchemyapi.io/v2/{ALCHEMY_API_KEY}'


POOL_CONTRACTS = {
    'CADC-USDC': '0xa6C0CbCaebd93AD3C6c94412EC06aaA37870216d',
    'EURS-USDC': '0x1a4Ffe0DCbDB4d551cfcA61A5626aFD190731347',
    'XSGD-USDC': '0x2baB29a12a9527a179Da88F422cDaaA223A90bD5',
    'NZDS-USDC': '0xe9669516e09f5710023566458f329cce6437aaac',
    'TRYB-USDC': '0xc574a613a3900e4314da13eb2287f13689a5b64d',
}
STAKING_CONTRACTS = {
    'CADC-USDC': '0x84Bf8151394dcF32146965753B28760550f3D7A8',
    'EURS-USDC': '0x5EaAEff69f2aB64d1CC0244FB31B236cA989544f',
    'XSGD-USDC': '0xd52D48Db08e8224ef6E2be8F54f3c84e790b1c32',
    'NZDS-USDC': '0xe06FA52e0d2D58Fe192285bfa0507F09cDd9824a',
    'TRYB-USDC': '0xdDB720069fdfE7BE2E2883A1c06BE0f353f7C4c8',    
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



def get_asset_transfers(currency_pair, deposits=True, request_id=0):
    label = 'deposits' if deposits else 'withdraws'
    cache_fp = f'{currency_pair}-{label}-{request_id}.json'
    if not os.path.exists(cache_fp):
        params = {
            'jsonrpc': '2.0',
            'method': 'alchemy_getAssetTransfers',
            'id': request_id,
            'params': [{
                'fromBlock': '0xCAB836',
                # 'toBlock': '0xCAB840',
                'maxCount': '0x3E8',
                'excludeZeroValue': True,
                'category': [
                    'external',
                    'token',
                ]
            }]
        }
        if deposits:
            params['params'][0]['toAddress'] = POOL_CONTRACTS[currency_pair]
        else:
            params['params'][0]['fromAddress'] = POOL_CONTRACTS[currency_pair]


        r = requests.post(ALCHEMY_BASE_URL, json=params)
        data = r.json()

        with open(cache_fp, 'w') as cache_f:
            json.dump(r.json(), cache_f)
    else:
        with open(cache_fp, 'r') as cache_f:
            data = json.load(cache_f)
    
    return data



if __name__ == '__main__':
    deposits_data = get_asset_transfers('TRYB-USDC', deposits=True, request_id=0)
    deposits_data = get_asset_transfers('TRYB-USDC', deposits=False, request_id=0)

