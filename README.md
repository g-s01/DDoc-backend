# UNDER-DEVELOPMENT

# DDoc - Decentralized issuing, verification and revoking of documents

This project was made as a solution to the problem statement by [Finance and Economics Club, IIT Guwahati](https://finnecoiitg.github.io/) in the Inter-Hostel Tech competition named [Kriti](https://kriti2024.onrender.com/). One can find the problem statement [here](PS.pdf).

## About

DDoc (**D**ecentralized **Doc**uments) aims to issue, verify and revoke documents by educational institutions in a decentralized manner.

## Requirements

* [truffle](https://trufflesuite.com/)
* [ganache](https://trufflesuite.com/ganache/)
* [streamlit](https://streamlit.io/)
* account on [Pinata](https://www.pinata.cloud/)

## Creating the `.env` file

One has to create a `.env` file for uploading documents on pinata

The structure of the `.env` file is:
```
PINATA_API (API key given by Pinata)
PINATA_SECRET (Secret Key given by Pinata)
```

## Running the file

To run the file, one can run the following commands:

* Run this is the project folder terminal
```
ganache-cli -h 127.0.0.1 -p 8545
```

* Open another terminal in the project folder and run this command
```
truffle migrate
```

* In the same terminal, run this command
```
streamlit run application/Home.py
```
