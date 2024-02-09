from web3 import Web3
from pathlib import Path
import json
import os
from eth_account import Account

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
path = 'build/contracts/Record.json'

def get_contract_address():
    try:
        ca = ""
        with open(path, 'r') as json_file:
            certification_data = json.load(json_file)
            transactions = certification_data.get('networks')
            # print(f"Transactions: {transactions}")
            for key, value in transactions.items():
                ca = value.get('address')
        print(f'Contract Address: {ca}')
        return ca
    except FileNotFoundError:
        print(f"Error: {path} not found.")
        return []

def get_contract_abi():
    try:
        with open(path, 'r') as json_file:
            certification_data = json.load(json_file)
            return certification_data.get('abi', [])
    except FileNotFoundError:
        print(f"Error: {path} not found.")
        return []
contract_abi = get_contract_abi()
contract_address = get_contract_address()
contract = w3.eth.contract(address=contract_address, abi=contract_abi)