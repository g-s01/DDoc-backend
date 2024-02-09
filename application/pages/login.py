import streamlit as st
from connect import contract, w3
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

st.title('login.py')

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

if submit:
    private_key, public_key = generate_keys()
    contract.functions.storeEmailAndPublicKey(email, public_key).transact({'from': w3.eth.accounts[0]})
    contract.functions.storeEmailAndPrivateKey(email, private_key).transact({'from': w3.eth.accounts[0]})
    st.success(f"Email and public key successfully stored for email ID: {email}")