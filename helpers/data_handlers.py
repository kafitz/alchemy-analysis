#!/usr/bin/env python

def get_next_block_num(transfers):
    return int(transfers[-1]['blockNum'], 16) + 1
