from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import os
import streamlit as st
from connect import contract, w3, account_address
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from dotenv import load_dotenv
from web3.middleware import geth_poa_middleware
from web3 import Web3
from cryptography.hazmat.primitives import serialization

load_dotenv()

# Load your account's private key (ensure this is securely managed)
wallet_private_key = os.getenv('PRIVATE_KEY')

def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    # Serialize private key to PEM format
    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serialize public key to PEM format
    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return pem_private_key, pem_public_key

email = st.text_input('Enter your email')
submit = st.button('Login')

# Usage example (replace 'contract_function_call' with your actual contract function call)
if submit:
    private_key, public_key = generate_keys()

    nonce = w3.eth.get_transaction_count(account_address)
    transaction = contract.functions.storeEmailAndPublicKey(email, public_key).build_transaction({
    'chainId': 11155111,  # Ethereum mainnet; change as necessary
    'gas': 2000000,
    'gasPrice': w3.to_wei('50', 'gwei'),
    'nonce': nonce,
    })

    # Sign transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=wallet_private_key)

    # Send transaction
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Get transaction receipt (may need to wait for transaction to be mined)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"Transaction successful with hash: {tx_receipt.transactionHash.hex()}")

    nonce = w3.eth.get_transaction_count(account_address)
    transaction = contract.functions.storeEmailAndPrivateKey(email, private_key).build_transaction({
    'chainId': 11155111,  # Ethereum mainnet; change as necessary
    'gas': 2000000,
    'gasPrice': w3.to_wei('50', 'gwei'),
    'nonce': nonce,
    })

    # Sign transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=wallet_private_key)

    # Send transaction
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Get transaction receipt (may need to wait for transaction to be mined)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"Transaction successful with hash: {tx_receipt.transactionHash.hex()}")

    st.success(f'Your email is {email} and your public key is securely stored on the blockchain.')