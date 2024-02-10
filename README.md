# DDoc - Decentralized issuing, verification, and revoking of documents

This project was made as a solution to the problem statement by [Finance and Economics Club, IIT Guwahati](https://finnecoiitg.github.io/) in the Inter-Hostel Tech competition named [Kriti](https://kriti2024.onrender.com/). One can find the problem statement [here](PS.pdf).

## About

DDoc (**D**ecentralized **Doc**uments) aims to issue, verify, and revoke documents by educational institutions in a decentralized manner.

## Requirements

* [truffle](https://trufflesuite.com/)
* [ganache](https://trufflesuite.com/ganache/)
* [streamlit](https://streamlit.io/)
* account on [Pinata](https://www.pinata.cloud/)

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

## Running the file

To run the file, one can run the following commands:

* Run this is the project folder terminal
```
streamlit run application/Home.py
```

* Note

One must have `Sepolia ETH` in their Metamask account to actually run this web app
