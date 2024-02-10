import streamlit as st
from connect import contract, w3

st.title('retrieve-public-key.py')

email = st.text_input('Enter your email')
submit = st.button('Login')

if submit:
    key = contract.functions.getPublicKey(email).call()
    st.write(f"Public key for email ID: {email} is: {key}")
    st.success(f"Public key successfully retrieved for email ID: {email}")