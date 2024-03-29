# DDoc - Decentralized issuing, verification, and revoking of documents

This project was made as a solution to the problem statement by [Finance and Economics Club, IIT Guwahati](https://finnecoiitg.github.io/) in the Inter-Hostel Tech competition named [Kriti](https://kriti2024.onrender.com/). One can find the problem statement [here](PS.pdf).

## About

DDoc (**D**ecentralized **Doc**uments) aims to issue, verify, and revoke documents by educational institutions in a decentralized manner.

## Requirements

* [truffle](https://trufflesuite.com/)
* [ganache](https://trufflesuite.com/ganache/)
* [streamlit](https://streamlit.io/)
* account on [Pinata](https://www.pinata.cloud/)

## Python library requirements

* `web3`
* `streamlit`
* `requests`
* `time`
* `cryptography.hazmat.backends`
* `cryptography.hazmat.primitives`
* `cryptography.hazmat.primitives.asymmetric`
* `dotenv`
* `os`
* `json`
* `PyPDF2`
* `hashlib`
* `cryptography.hazmat.primitives.serialization`
* `web3.middleware`
* `eth_account`
* `pathlib`
* `reportlab.lib.pagesizes`
* `reportlab.platypus`
* `reportlab.lib.styles`
* `pdfplumber`

## Creating the `.env` file

One has to create a `.env` file for uploading documents on Pinata

The structure of the `.env` file is:
```
PINATA_API (API key given by Pinata)
PINATA_SECRET (Secret Key given by Pinata)
ABI (deployed contract ABI)
CONTRACT_ADDRESS (deployed contract address)
ACCOUNT (Metamask wallet public key)
PRIVATE_KEY (Metamask wallet private key)
```

`Contract DEPLOYED on SEPOLIA Network: 0x04b3AdDF4e17e5f3af108456785a1450eE5Aa18C`

## Running the file

To run the file, one can run the following commands:

* Run this is the project folder terminal
```
streamlit run application/Home.py
```

# Note

One must have `Sepolia ETH` on Metamask account `0xB9b7444621afC6c6f3028434e675Cf974085957c` to actually run this web app
