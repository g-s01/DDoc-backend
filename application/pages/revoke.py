import streamlit as st
import os
import hashlib
from dotenv import load_dotenv
from connect import contract, w3, account_address

st.title('revoke.py')

load_dotenv()

documentName = st.text_input('Enter the document name')
recipientEmail = st.text_input('Enter the recipient email')
orgEmail = st.text_input('Enter the organization email')
submit = st.button('Revoke')

if submit:
    data_to_hash = f"{documentName}{recipientEmail}{orgEmail}".encode('utf-8')
    documentId = hashlib.sha256(data_to_hash).hexdigest()
    wallet_private_key = os.getenv('PRIVATE_KEY')
    nonce = w3.eth.get_transaction_count(account_address)
    transaction = contract.functions.revokeDocument(documentId).build_transaction({
        'chainId': 11155111,  # Ethereum mainnet; change as necessary
        'gas': 2000000,
        'gasPrice': w3.to_wei('50', 'gwei'),
        'nonce': nonce,
    })
    st.success(f"Document with ID: {documentId} successfully revoked")
