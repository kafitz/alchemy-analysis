#!/usr/bin/env python

BLACKHOLE_ADDRESS = '0x0000000000000000000000000000000000000000'

TOKENS = {
    'CADC': '0xcadc0acd4b445166f12d2c07eac6e2544fbe2eef',
    'EURS': '0x1a4ffe0dcbdb4d551cfca61a5626afd190731347',
    'NZDS': '0xda446fad08277b4d2591536f204e018f32b6831c',
    'USDC': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
    'TRYB': '0x2C537E5624e4af88A7ae4060C022609376C8D0EB',
    'XSGD': '0x70e8de73ce538da2beed35d14187f6959a8eca96',
}

POOL_CONTRACTS = {
    'CADC-USDC': ('0xa6C0CbCaebd93AD3C6c94412EC06aaA37870216d', 12459301),
    'EURS-USDC': ('0x1a4Ffe0DCbDB4d551cfcA61A5626aFD190731347', 12459337),
    'NZDS-USDC': ('0xe9669516e09f5710023566458f329cce6437aaac', 13234461),
    'TRYB-USDC': ('0xc574a613a3900e4314da13eb2287f13689a5b64d', 13283851),
    'XSGD-USDC': ('0x2baB29a12a9527a179Da88F422cDaaA223A90bD5', 12459348),
}
STAKING_CONTRACTS = {
    'CADC-USDC': ('0x84Bf8151394dcF32146965753B28760550f3D7A8', 12459404),
    'EURS-USDC': ('0x5EaAEff69f2aB64d1CC0244FB31B236cA989544f', 12459411),
    'NZDS-USDC': ('0xe06FA52e0d2D58Fe192285bfa0507F09cDd9824a', 13232886),
    'TRYB-USDC': ('0xdDB720069fdfE7BE2E2883A1c06BE0f353f7C4c8', 13282257),
    'XSGD-USDC': ('0xd52D48Db08e8224ef6E2be8F54f3c84e790b1c32', 12459420),
}
ZAP_CONTRACT_INFO = ('0x64d65E3d70ba0f8812A9d1d7b8B5C51DAB78CD15', 12600535)

class CURRENCIES:
    CADC = 'CADC'
    EURS = 'EURS'
    NZDS = 'NZDS'
    TRYB = 'TRYB'
    USDC = 'USDC'
    XSGD = 'XSGD'

DIVISORS = {
    'CADC': 1E18,
    'EURS': 1E2,
    'NZDS': 1E6,
    'TRYB': 1E6,
    'USDC': 1E6,
    'XSGD': 1E6,
    'dfx-cadc-a': 1E18,
    'dfx-eurs-a': 1E18,
    'dfx-nzds-a': 1E18,
    'dfx-tryb-a': 1E18,
    'dfx-xsgd-a': 1E18,
}
