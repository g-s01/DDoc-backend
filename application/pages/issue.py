import requests
import json
import os
from dotenv import load_dotenv
import hashlib
import streamlit as st
from utils.doc_utils import generate_certificate
from connect import contract, w3

st.title('issue.py')

load_dotenv()

api_key = os.getenv("PINATA_API")
api_secret = os.getenv("PINATA_SECRET")

def upload_to_pinata(file_path, api_key, api_secret):
    # Set up the Pinata API endpoint and headers
    pinata_api_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": api_key,
        "pinata_secret_api_key": api_secret,
    }

    # Prepare the file for upload
    with open(file_path, "rb") as file:
        files = {"file": (file.name, file)}

        # Make the request to Pinata
        response = requests.post(pinata_api_url, headers=headers, files=files)

        # Parse the response
        result = json.loads(response.text)

        if "IpfsHash" in result:
            ipfs_hash = result["IpfsHash"]
            print(f"File uploaded to Pinata. IPFS Hash: {ipfs_hash}")
            return ipfs_hash
        else:
            print(f"Error uploading to Pinata: {result.get('error', 'Unknown error')}")
            return None

form = st.form(key='Issue Document to someone!')
documentName = form.text_input('Document Name')
recipientEmail = form.text_input('Recipient Email')
orgEmail = form.text_input('Organization Email')
cpi = form.text_input('CPI')
submit = form.form_submit_button('Issue')

if submit:
    pdf_file_path = "certificate.pdf"
    # institute_logo_path = "../assets/iitg_logo.jpg"
    generate_certificate(documentName, recipientEmail, orgEmail, cpi, pdf_file_path)
    # Upload the PDF to Pinata
    ipfsHash = upload_to_pinata(pdf_file_path, api_key, api_secret)
    os.remove(pdf_file_path)
    data_to_hash = f"{documentName}{recipientEmail}{orgEmail}{cpi}".encode('utf-8')
    documentId = hashlib.sha256(data_to_hash).hexdigest()

    # Smart Contract Call
    contract.functions.issueDocument(documentId, recipientEmail, ipfsHash, ipfsHash, orgEmail).transact({'from': w3.eth.accounts[0]})
    st.success(f"Certificate successfully generated with Certificate ID: {documentId}")