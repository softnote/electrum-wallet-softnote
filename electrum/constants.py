# -*- coding: utf-8 -*-
#
# Electrum - lightweight Softnote client
# Copyright (C) 2018 The Electrum developers
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import json

from .util import inv_dict, all_subclasses
from . import softnote


def read_json(filename, default):
    path = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(path, 'r') as f:
            r = json.loads(f.read())
    except:
        r = default
    return r


GIT_REPO_URL = "https://github.com/softnote/electrum"
GIT_REPO_ISSUES_URL = "https://github.com/softnote/electrum/issues"
BIP39_WALLET_FORMATS = read_json('bip39_wallet_formats.json', [])


class AbstractNet:

    NET_NAME: str
    TESTNET: bool
    WIF_PREFIX: int
    ADDRTYPE_P2PKH: int
    ADDRTYPE_P2SH: int
    SEGWIT_HRP: str
    BOLT11_HRP: str
    GENESIS: str
    BLOCK_HEIGHT_FIRST_LIGHTNING_CHANNELS: int = 0
    BIP44_COIN_TYPE: int
    LN_REALM_BYTE: int

    @classmethod
    def max_checkpoint(cls) -> int:
        return max(0, len(cls.CHECKPOINTS) * 2016 - 1)

    @classmethod
    def rev_genesis_bytes(cls) -> bytes:
        return bytes.fromhex(softnote.rev_hex(cls.GENESIS))


class SoftnoteMainnet(AbstractNet):

    NET_NAME = "mainnet"
    TESTNET = False
    WIF_PREFIX = 0x80
    ADDRTYPE_P2PKH = 8
    ADDRTYPE_P2SH = 18
    SEGWIT_HRP = "sf"
    BOLT11_HRP = SEGWIT_HRP
    GENESIS = "00000000579fb2c32b1df9ae58bb0c23b89fafe69a8a40dffa5835653a177b1e"
    DEFAULT_PORTS = {'t': '54001', 's': '54002'}
    DEFAULT_SERVERS = read_json('servers.json', {})
    CHECKPOINTS = read_json('checkpoints.json', [])
    BLOCK_HEIGHT_FIRST_LIGHTNING_CHANNELS = 100000

    XPRV_HEADERS = {
        'standard':    0x6288ade4,  # xprv
        'p2wpkh-p2sh': 0x049d7878,  # yprv
        'p2wsh-p2sh':  0x0295b005,  # Yprv
        'p2wpkh':      0x04b2430c,  # zprv
        'p2wsh':       0x02aa7a99,  # Zprv
    }
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)
    XPUB_HEADERS = {
        'standard':    0x6288b21e,  # xpub
        'p2wpkh-p2sh': 0x049d7cb2,  # ypub
        'p2wsh-p2sh':  0x0295b43f,  # Ypub
        'p2wpkh':      0x04b24746,  # zpub
        'p2wsh':       0x02aa7ed3,  # Zpub
    }
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)
    BIP44_COIN_TYPE = 0
    LN_REALM_BYTE = 0
    LN_DNS_SEEDS = [ ]


class SoftnoteTestnet(AbstractNet):

    NET_NAME = "testnet"
    TESTNET = True
    WIF_PREFIX = 0xef
    ADDRTYPE_P2PKH = 121
    ADDRTYPE_P2SH = 33
    SEGWIT_HRP = "ts"
    BOLT11_HRP = SEGWIT_HRP
    GENESIS = "00000000368e1d05913204a1191bd808dc3f8be260fddaef97621a12eed9753d"
    DEFAULT_PORTS = {'t': '54003', 's': '54004'}
    DEFAULT_SERVERS = read_json('servers_testnet.json', {})
    CHECKPOINTS = read_json('checkpoints_testnet.json', [])

    XPRV_HEADERS = {
        'standard':    0x62358394,  # tprv
        'p2wpkh-p2sh': 0x044a4e28,  # uprv
        'p2wsh-p2sh':  0x024285b5,  # Uprv
        'p2wpkh':      0x045f18bc,  # vprv
        'p2wsh':       0x02575048,  # Vprv
    }
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)
    XPUB_HEADERS = {
        'standard':    0x623587cf,  # tpub
        'p2wpkh-p2sh': 0x044a5262,  # upub
        'p2wsh-p2sh':  0x024289ef,  # Upub
        'p2wpkh':      0x045f1cf6,  # vpub
        'p2wsh':       0x02575483,  # Vpub
    }
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)
    BIP44_COIN_TYPE = 1
    LN_REALM_BYTE = 1
    LN_DNS_SEEDS = [  # TODO investigate this again
        #'test.nodes.lightning.directory.',  # times out.
        #'lseed.softnotestats.com.',  # ignores REALM byte and returns mainnet peers...
    ]


class SoftnoteRegtest(SoftnoteTestnet):

    NET_NAME = "regtest"
    SEGWIT_HRP = "sfrt"
    BOLT11_HRP = SEGWIT_HRP
    GENESIS = "11e7891d3cdebf71550f81b278b225b0698175ad41d855977a96b69882677048"
    DEFAULT_SERVERS = read_json('servers_regtest.json', {})
    CHECKPOINTS = []
    LN_DNS_SEEDS = []





class SoftnoteSignet(SoftnoteTestnet):

    NET_NAME = "signet"
    BOLT11_HRP = "tss"
    GENESIS = "0000023a16958313160ff508a5b5b010f87c0d9954c07b8f86178a3a19348554"
    DEFAULT_SERVERS = read_json('servers_signet.json', {})
    CHECKPOINTS = []
    LN_DNS_SEEDS = []


NETS_LIST = tuple(all_subclasses(AbstractNet))

# don't import net directly, import the module instead (so that net is singleton)
net = SoftnoteMainnet

def set_signet():
    global net
    net = SoftnoteSignet



def set_mainnet():
    global net
    net = SoftnoteMainnet

def set_testnet():
    global net
    net = SoftnoteTestnet

def set_regtest():
    global net
    net = SoftnoteRegtest
