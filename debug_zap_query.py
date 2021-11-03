from pprint import pprint
import requests

from config import ALCHEMY_BASE_URL
from constants import POOL_CONTRACTS, ZAP_CONTRACTS



def test_request_alchemy_zap(contract_address, start_block, deposit=False, withdrawal=False, zap=False):
    params = {
        'jsonrpc': '2.0',
        'method': 'alchemy_getAssetTransfers',
        'id': 0,
        'params': [{
            'fromBlock': hex(start_block),
            'toBlock': hex(start_block + 1),
            # 'maxCount': hex(10),
            'excludeZeroValue': True,
            'category': [
                'external',
                'token',
            ]
        }]
    }

    if deposit:
        params['params'][0]['toAddress'] = contract_address
    elif withdrawal:
        params['params'][0]['fromAddress'] = contract_address
    elif zap:
        params['params'][0]['contractAddresses'] = [contract_address]
        # params['params'][0]['fromAddress'] = contract_address

    r = requests.post(ALCHEMY_BASE_URL, json=params)
    data = r.json()
    return data


contract_address = ZAP_CONTRACTS['TRYB-USDC']
start_block = 13285996

# print('Deposits:')
# pprint(test_request_alchemy_zap(contract_address, start_block, deposit=True))
# print('Withdrawals:')
# pprint(test_request_alchemy_zap(contract_address, start_block, withdrawal=True))
print('Zap:')
pprint(test_request_alchemy_zap(contract_address, start_block, zap=True))
