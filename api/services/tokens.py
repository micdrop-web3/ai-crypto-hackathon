import os

from eth_account import Account
from web3 import Web3
from web3.middleware import construct_sign_and_send_raw_middleware

ABI = [
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"},
        ],
        "name": "transfer",
        "outputs": [],
        "payable": False,
        "type": "function",
    },
]


def transfer_erc20(client, chain_id, contract_addr, to_addr, value):
    contract_addr = Web3.toChecksumAddress(contract_addr)
    contract = client.eth.contract(address=contract_addr, abi=ABI)
    tx_hash = contract.functions.transfer(to_addr, value).transact()
    return tx_hash


def get_web3_client():
    client = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URL")))
    client.chain_id = int(os.getenv("WEB3_CHAIN_ID"))
    # 良い子のみんなはEOAの秘密鍵を厳重に管理しよう！
    account = Account.from_key(os.getenv("WEB3_SECRET_KEY"))
    middleware = construct_sign_and_send_raw_middleware(account)
    client.middleware_onion.add(middleware)
    return client
