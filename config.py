#!/usr/bin/env python
import dotenv
import os

dotenv.load_dotenv()


ALCHEMY_API_KEY = os.environ.get('ALCHEMY_API_KEY')
ALCHEMY_BASE_URL = f'https://eth-mainnet.alchemyapi.io/v2/{ALCHEMY_API_KEY}'

DATA_DIR = '.'
