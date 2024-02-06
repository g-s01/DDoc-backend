from web3 import Web3
import streamlit as st
from connect import contract
import requests
import time

st.title('get.py')

email = st.text_input('Enter your email')
submit = st.button('Get Certificates')

if submit:
    url = 'https://gateway.pinata.cloud/ipfs/'
    documentIds = contract.functions.getDocument(email).call()
    for item, org in documentIds:
        temp_url = url + item
        st.write(temp_url)
        st.write(org)
    st.success(f"Certificates successfully fetched for email ID: {email}")