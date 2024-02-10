import PyPDF2
from web3 import Web3
import os
import hashlib
from dotenv import load_dotenv
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from web3.middleware import geth_poa_middleware

load_dotenv()
w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/876416b64f21409c820da8ef84e7c529'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
private_key = os.getenv('PRIVATE_KEY')

account = w3.eth.account.from_key(private_key)
account_address = account.address

# Function to hash a string using SHA-256
def hash_string(input_string):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(input_string.encode('utf-8'))
    return digest.finalize()

def find_hash_of_pdf_contents(pdf_path):
    input_string = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            input_string += page.extract_text()
    hashed_message = hash_string(input_string)
    return hashed_message
    

def extract_signature_from_pdf(pdf_path):
    # Read the PDF
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        # Access the metadata
        metadata = reader.metadata
        # Extract the signature
        signature = metadata.get('/Signature')
        if signature:
            # If the signature was stored as a string, convert it back to bytes
            signature_bytes = signature.encode('latin1')
            return signature_bytes
        else:
            print("No signature found in PDF metadata.")
            return None
        
def verify_with_public_key(public_key, message, signature):
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print(f'Verification failed: {str(e)}')
        return False

def verify(orgEmail, recipientEmail, docname, pdf_path):
    publicKey = contract.functions.getPublicKey(orgEmail).call()
    public_key = load_pem_public_key(publicKey, backend=default_backend())
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    hashed_message = find_hash_of_pdf_contents(pdf_path)
    data_to_hash = f"{docname}{recipientEmail}{orgEmail}".encode('utf-8')
    documentId = hashlib.sha256(data_to_hash).hexdigest()
    print(documentId)
    if(contract.functions.isDocumentExist(documentId).call() == False):
        print("Document does not exist")
        return False
    print(hashed_message)
    signature = extract_signature_from_pdf(pdf_path)
    print(signature)
    print(public_key)
    verification_result = verify_with_public_key(public_key, hashed_message, signature)
    return verification_result

# print(verify('g.adittya@iitg.ac.in', 'gautam.sharma@iitg.ac.in', 'yo', '/Users/gautamsharma/Desktop/QmfKQ9vDKsXL3rPWjh2KBdvXEbkgqjnc8pfqeWCWP6kDj3.pdf'))