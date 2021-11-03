#!/usr/bin/env python
import config
from helpers import file_handlers

config.DATA_DIR = './tests/test-data'


def test_file_handlers():
    assert file_handlers.get_or_init_request_idx('NZDS-USDC', 'deposits') == 1


def test_load_next_block_from_file():
    assert file_handlers.load_next_block('NZDS-USDC', 'deposits', 0) == 13539814

