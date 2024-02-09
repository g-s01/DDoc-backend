import requests
import json
import os
import PyPDF2
from dotenv import load_dotenv
import hashlib
import streamlit as st
from utils.doc_utils import generate_certificate
from connect import contract, w3
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

st.title('issue.py')

load_dotenv()

api_key = os.getenv("PINATA_API")
api_secret = os.getenv("PINATA_SECRET")

def hash_string(input_string):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(input_string.encode('utf-8'))
    return digest.finalize()

# Function to encrypt a message using a public key
def encrypt_with_public_key(public_key, message):
    encrypted_message = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
    )
    return encrypted_message

def sign_with_private_key(private_key, message):
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature
    
#method to append digital signature to pdf
def append_signature_to_pdf(input_pdf_path, output_pdf_path, signature_bytes):
    # Read the existing PDF
    with open(input_pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        # Add all pages to the writer
        for page in reader.pages:
            writer.add_page(page)

        # Add the signature as metadata
        metadata = reader.metadata
        metadata.update({
            '/Signature': PyPDF2.generic.create_string_object(signature_bytes.decode('latin1'))
        })
        writer.add_metadata(metadata)

        # Write the new PDF to a file
        with open(output_pdf_path, 'wb') as output_file:
            writer.write(output_file)

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
            # print(f"File uploaded to Pinata. IPFS Hash: {ipfs_hash}")
            return ipfs_hash
        else:
            st.write(f"Error uploading to Pinata: {result.get('error', 'Unknown error')}")
            return None

form = st.form(key='Issue Document to someone!')
documentName = form.text_input('Document Name')
recipientEmail = form.text_input('Recipient Email')
orgEmail = form.text_input('Organization Email')
cpi = form.text_input('CPI')
submit = form.form_submit_button('Issue')

if submit:
    privateKey = contract.functions.getPrivateKey(orgEmail).call() 
    private_key = serialization.load_pem_private_key(
        privateKey,
        password=None,  # Use a password if your key is encrypted
    )
    pdf_file_path = "certificate.pdf"
    generate_certificate(documentName, recipientEmail, orgEmail, cpi, pdf_file_path)
    with open('certificate.pdf', 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        input_string = ""
        for page in reader.pages:
            input_string += page.extract_text()
    hashed_message = hash_string(input_string)
    # Sign the hashed message with private key
    signature = sign_with_private_key(private_key, hashed_message)
    input_pdf_path = 'certificate.pdf'
    output_pdf_path = 'VC_ceritificate.pdf'
    # Append the signature to the PDF
    append_signature_to_pdf(input_pdf_path, output_pdf_path, signature)
    # Upload the PDF to Pinata
    ipfsHash = upload_to_pinata(output_pdf_path, api_key, api_secret)
    publicKey = contract.functions.getPublicKey(recipientEmail).call()
    public_key = load_pem_public_key(publicKey, backend=default_backend())
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    public_key = serialization.load_pem_public_key(
        pem,
        backend=default_backend()
    )
    ciphertext = encrypt_with_public_key(public_key, ipfsHash.encode('utf-8'))
    os.remove(pdf_file_path)
    os.remove("VC_ceritificate.pdf")
    data_to_hash = f"{documentName}{recipientEmail}{orgEmail}{cpi}".encode('utf-8')
    documentId = hashlib.sha256(data_to_hash).hexdigest()

    # Smart Contract Call
    contract.functions.issueDocument(documentId, recipientEmail, ciphertext, orgEmail).transact({'from': w3.eth.accounts[0]})
    st.success(f"Certificate successfully generated with Certificate ID: {documentId}")