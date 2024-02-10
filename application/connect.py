from web3 import Web3
from pathlib import Path
import json
import os
from eth_account import Account
from dotenv import load_dotenv
from web3.middleware import geth_poa_middleware

load_dotenv()

w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/876416b64f21409c820da8ef84e7c529'))
path = 'build/contracts/Record.json'
private_key = os.getenv('PRIVATE_KEY')

w3.middleware_onion.inject(geth_poa_middleware, layer=0)

account = w3.eth.account.from_key(private_key)
account_address = account.address

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

contract_abi = '[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"recipientEmail","type":"string"},{"indexed":false,"internalType":"bytes","name":"ipfsHashSigned","type":"bytes"},{"indexed":false,"internalType":"string","name":"orgEmail","type":"string"}],"name":"documentIssued","type":"event"},{"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"documents","outputs":[{"internalType":"string","name":"documentName","type":"string"},{"internalType":"string","name":"recipientEmail","type":"string"},{"internalType":"bytes","name":"ipfsHashSigned","type":"bytes"},{"internalType":"string","name":"orgEmail","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"email","type":"string"}],"name":"getDocument","outputs":[{"components":[{"internalType":"bytes","name":"documentHash","type":"bytes"},{"internalType":"string","name":"documentName","type":"string"},{"internalType":"string","name":"orgEmail","type":"string"}],"internalType":"struct Record.DocumentHashAndDocumentNameAndOrgEmail[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"email","type":"string"}],"name":"getPrivateKey","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"email","type":"string"}],"name":"getPublicKey","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"documentId","type":"string"}],"name":"isDocumentExist","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"documentId","type":"string"},{"internalType":"string","name":"documentName","type":"string"},{"internalType":"string","name":"recipientEmail","type":"string"},{"internalType":"bytes","name":"ipfsHashSigned","type":"bytes"},{"internalType":"string","name":"orgEmail","type":"string"}],"name":"issueDocument","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"recipientEmailAndDocumentNameAndDocumentHashAndOrgEmails","outputs":[{"internalType":"string","name":"recipientEmail","type":"string"},{"internalType":"string","name":"documentName","type":"string"},{"internalType":"bytes","name":"documentHash","type":"bytes"},{"internalType":"string","name":"orgEmail","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"recipientEmailAndPrivateKeys","outputs":[{"internalType":"string","name":"recipientEmail","type":"string"},{"internalType":"bytes","name":"privateKey","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"recipientEmailAndPublicKeys","outputs":[{"internalType":"string","name":"recipientEmail","type":"string"},{"internalType":"bytes","name":"publicKey","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"documentId","type":"string"}],"name":"revokeDocument","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"email","type":"string"},{"internalType":"bytes","name":"privateKey","type":"bytes"}],"name":"storeEmailAndPrivateKey","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"email","type":"string"},{"internalType":"bytes","name":"publicKey","type":"bytes"}],"name":"storeEmailAndPublicKey","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
contract_address = "0x644e96f2785E3B531a1B29ABaa833F9e0606F762"
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

account = w3.eth.account.from_key(private_key)
account_address = account.address