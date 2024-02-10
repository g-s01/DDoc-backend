from web3 import Web3
import streamlit as st
import requests
import time
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from dotenv import load_dotenv
import os
from connect import contract

def decrypt_with_private_key(private_key, ciphertext):
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext

st.title('get.py')

email = st.text_input('Enter your email')
submit = st.button('Get Certificates')

if submit:
    url = 'https://gateway.pinata.cloud/ipfs/'
    ppriv = contract.functions.getPrivateKey(email).call()
    ppriv = serialization.load_pem_private_key(
        ppriv,
        password=None,
    )
    documentIds = contract.functions.getDocument(email).call()
    for item, name, org in documentIds:
        item = decrypt_with_private_key(ppriv, item)
        item = item.decode('utf-8')
        temp_url = url + item
        st.write(item)
        st.write(name)
        st.write(org)
    st.success(f"Certificates successfully fetched for email ID: {email}")