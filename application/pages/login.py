import streamlit as st
from connect import contract, w3

st.title('login.py')

email = st.text_input('Enter your email')
public_key = st.text_input('Enter your public key')
submit = st.button('Login')

if submit:
    contract.functions.storeEmailAndDocumentHash(email, public_key).transact({'from': w3.eth.accounts[0]})
    st.success(f"Email and public key successfully stored for email ID: {email}")