#!/usr/bin/env python
import json
import os

import config
from helpers import data_handlers


def get_or_init_request_idx(currency_pair, tx_type):
    new_idx = 0
    for fn in sorted(os.listdir(config.DATA_DIR)):
        if currency_pair in fn:
            base_fn_parts = fn.rstrip('.json').split('-')
            if base_fn_parts[2] != tx_type:
                continue
            new_idx = int(base_fn_parts[-1]) + 1
    return new_idx


def load_next_block(currency_pair, tx_type, request_id):
    cache_fp = os.path.join(config.DATA_DIR, f'{currency_pair}-{tx_type}-{request_id}.json')
    with open(cache_fp, 'r') as cache_f:
        data = json.load(cache_f)
    print(data['result']['transfers'])
    next_block = data_handlers.get_next_block_num(data['result']['transfers'])
    return next_block
