#!/usr/bin/env python
from helpers import data_handlers

def test_get_next_block_num():
    test_data = [
        {'blockNum': '0xce4513', 'hash': '0x72b0bdd33b5503e7bdd841aa6b79a93b86def53d5226391390f7f1067c1d8585', 'from': '0x64d65e3d70ba0f8812a9d1d7b8b5c51dab78cd15', 'to': '0xe9669516e09f5710023566458f329cce6437aaac', 'value': 23101.94628, 'erc721TokenId': None, 'erc1155Metadata': None, 'asset': 'USDC', 'category': 'token', 'rawContract': {'value': '0x0560fbb9a8', 'address': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 'decimal': '0x6'}},
        {'blockNum': '0xce4513', 'hash': '0x72b0bdd33b5503e7bdd841aa6b79a93b86def53d5226391390f7f1067c1d8585', 'from': '0x64d65e3d70ba0f8812a9d1d7b8b5c51dab78cd15', 'to': '0xe9669516e09f5710023566458f329cce6437aaac', 'value': None, 'erc721TokenId': None, 'erc1155Metadata': None, 'asset': None, 'category': 'token', 'rawContract': {'value': '0x077f8a59ba', 'address': '0xda446fad08277b4d2591536f204e018f32b6831c', 'decimal': None}},
        {'blockNum': '0xce7efe', 'hash': '0x7a9ef0fc9e2e0087b39da8ec6e7798caa645660c9fe0d7e57264dd862eb81452', 'from': '0x9d0950c595786aba7c26dfddf270d66a8b18b4fa', 'to': '0xe9669516e09f5710023566458f329cce6437aaac', 'value': None, 'erc721TokenId': None, 'erc1155Metadata': None, 'asset': None, 'category': 'token', 'rawContract': {'value': '0x407347eb00', 'address': '0xda446fad08277b4d2591536f204e018f32b6831c', 'decimal': None}},
        {'blockNum': '0xce99e5', 'hash': '0x69f4fc6a939452757342adbbc94a0d9b64a0cbe7e2a9d0a1dc62c342235a63e0', 'from': '0x9d0950c595786aba7c26dfddf270d66a8b18b4fa', 'to': '0xe9669516e09f5710023566458f329cce6437aaac', 'value': None, 'erc721TokenId': None, 'erc1155Metadata': None, 'asset': None, 'category': 'token', 'rawContract': {'value': '0x746a528800', 'address': '0xda446fad08277b4d2591536f204e018f32b6831c', 'decimal': None}}
    ]
    assert data_handlers.get_next_block_num(test_data) == 13539814


def test__get_asset():
    test_data = {
        'blockNum': '0xcab20b', 
        'hash': '0x1bc2279eab59f8fb7c5b581abcecbe5ce241c05bf584866bbd3e5939b67d58ad',
        'from': None,
        'to': None,
        'value': 900,
        'erc721TokenId': None,
        'erc1155Metadata': None,
        'asset': None,
        'category': 'token',
        'rawContract': {
            'value': '0x35a4e900',
            'address': None,
            'decimal': '0x6'
        }
    }

    test_data_asset = dict(test_data)
    test_data_asset['asset'] = 'TRYB'
    assert data_handlers._get_asset(test_data_asset) == 'TRYB'

    test_data_asset = dict(test_data)
    test_data_asset['to'] = '0x2C537E5624e4af88A7ae4060C022609376C8D0EB'
    assert data_handlers._get_asset(test_data_asset) == 'TRYB'

    test_data_asset = dict(test_data)
    test_data_asset['from'] = '0x2C537E5624e4af88A7ae4060C022609376C8D0EB'
    assert data_handlers._get_asset(test_data_asset) == 'TRYB'

    test_data_asset = dict(test_data)
    test_data_asset['rawContract']['address'] = '0x2C537E5624e4af88A7ae4060C022609376C8D0EB'
    assert data_handlers._get_asset(test_data_asset) == 'TRYB'            
