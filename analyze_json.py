#!/usr/bin/env python
import json
from pprint import pprint


def process_deposits(currency_pair, request_id):
    cache_fp = f'{currency_pair}-deposits-{request_id}.json'
    with open(cache_fp, 'r') as cache_f:
        data = json.load(cache_f)

    for transfer in data['result']['transfers']:
        print(transfer)
        break


if __name__ == '__main__':
    process_deposits('TRYB-USDC', request_id=0)

