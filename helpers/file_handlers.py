#!/usr/bin/env python
import json
import os

import config
from helpers import data_handlers


def _create_fn(cur1, cur2, tx_type, request_id):
    return f'{cur1}-{cur2}-{tx_type}-{request_id}.json'


# returns a request idx following any existing cached file ids or 0
def get_or_init_request_idx(currency_pair, tx_type):
    new_idx = 0
    for fn in sorted(os.listdir(config.DATA_DIR)):
        if currency_pair in fn:
            base_fn_parts = fn.rstrip('.json').split('-')
            if base_fn_parts[2] != tx_type:
                continue
            new_idx = int(base_fn_parts[-1]) + 1
    return new_idx


# returns a zap request idx following any existing cached file ids or 0
def get_or_init_zap_request_idx(tx_type):
    new_idx = 0
    for fn in sorted(os.listdir(config.DATA_DIR)):
        if 'zap-contract' in fn:
            base_fn_parts = fn.rstrip('.json').split('-')
            if base_fn_parts[2] != tx_type:
                continue
            new_idx = int(base_fn_parts[-1]) + 1
    return new_idx    


# return the next block number following the most recently cached block number
def load_next_block(currency_pair, tx_type, request_id):
    cur1, cur2 = currency_pair.split('-')
    cache_fp = os.path.join(config.DATA_DIR, _create_fn(cur1, cur2, tx_type, request_id))
    with open(cache_fp, 'r') as cache_f:
        data = json.load(cache_f)
    next_block = data_handlers.get_next_block_num(data['result']['transfers'])
    return next_block


def load_next_zap_block(tx_type, request_id):
    cache_fp = os.path.join(config.DATA_DIR, f'zap-contract-{tx_type}-{request_id}.json')
    with open(cache_fp, 'r') as cache_f:
        data = json.load(cache_f)
    next_block = data_handlers.get_next_block_num(data['result']['transfers'])
    return next_block


# iterate over cache data files in order and concatenate contents
def _load_all_data(cur1, cur2, tx_type):
    mock_json = {'result': { 'transfers': [] }}  # return a mock json response for legibility
    json_fns = [fn for fn in os.listdir(config.DATA_DIR) if fn.endswith('.json')]
    for fn in sorted(json_fns):
        is_match = fn.startswith(f'{cur1}-{cur2}-{tx_type}-')
        if is_match:
            cache_fp = os.path.join(config.DATA_DIR, fn)
            with open(cache_fp, 'r') as cache_f:
                data = json.load(cache_f)
            mock_json['result']['transfers'].extend(data['result']['transfers'])
    return mock_json

def _load_all_zap_data(tx_type):
    mock_json = {'result': { 'transfers': [] }}  # return a mock json response for legibility
    json_fns = [fn for fn in os.listdir(config.DATA_DIR) if fn.endswith('.json')]
    for fn in sorted(json_fns):
        is_match = fn.startswith(f'zap-contract-{tx_type}-')
        if is_match:
            cache_fp = os.path.join(config.DATA_DIR, fn)
            with open(cache_fp, 'r') as cache_f:
                data = json.load(cache_f)
            mock_json['result']['transfers'].extend(data['result']['transfers'])
    return mock_json    


# iterate over json file and generate a list of formatted transactions
def load_cached_data(cur1, cur2, deposit=False, withdrawal=False):
    if deposit:
        data = _load_all_data(cur1, cur2, 'deposits')
    elif withdrawal:
        data = _load_all_data(cur1, cur2, 'withdrawals')
    else:
        raise Exception('Cached data type not specified.')

    return data_handlers.format_transfers(data)


def load_cached_zap_data(deposit=False, withdrawal=False):
    if deposit:
        data = _load_all_zap_data('deposits')
    elif withdrawal:
        data = _load_all_zap_data('withdrawals')
    else:
        raise Exception('Cached data type not specified.')
    return data_handlers.format_transfers(data)