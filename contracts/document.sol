// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.9;

/// @title A contract to issue/get/revoke documents to anyone
/// @author g-s01
/// @notice A contract to issue/get/revoke documents to anyone
/// @dev Verification of the document is not implemented, and will be done somewhere else
contract Record{
    // A document can be uniquely identified by the recipient's email,
    // the hash of the document on IPFS
    // and the email of the organization that issued the document
    struct Document{
        string recipientEmail;
        string ipfsHash;
        string ipfsHashSignedWithPrivateKey;
        string orgEmail;
    }
    struct emailAndDocumentHash{
        string email;
        string documentHash;
    }
    struct emailAndPublicKey{
        string email;
        string publicKey;
    }
    emailAndPublicKey[] public emailAndPublicKeys;
    emailAndDocumentHash[] public emailAndDocumentHashs;
    // A mapping from the document ID to the document
    mapping(string => Document) public documents;
    // An event that is emitted when a document is issued
    event documentIssued(string recipientEmail, string ipfsHash, string ipfsHashSignedWithPrivateKey, string orgEmail);
    // Modifier to check whether the certificate is original or not
    modifier isOriginal(string memory documentId){
        require(
            bytes(documents[documentId].ipfsHash).length == 0,
            "This document is not original"
        );
        _;
    }
    // Modifier to check whether the certificate exists or not
    modifier isExist(string memory documentId){
        require(
            bytes(documents[documentId].ipfsHash).length != 0,
            "This document does not exist"
        );
        _;
    }
    // A function to issue a document
    function issueDocument(
        string memory documentId,
        string memory recipientEmail,
        string memory ipfsHash,
        string memory ipfsHashSignedWithPrivateKey,
        string memory orgEmail
    ) public isOriginal (ipfsHash){
        Document memory newDocument = Document(
            recipientEmail,
            ipfsHash,
            ipfsHashSignedWithPrivateKey,
            orgEmail
        );
        documents[documentId] = newDocument;
        emailAndDocumentHashs.push(emailAndDocumentHash(recipientEmail, ipfsHash));
        emit documentIssued(recipientEmail, ipfsHash, ipfsHashSignedWithPrivateKey, orgEmail);
    }
    // A function to get certificates for a particular email
    function getDocument(string memory email)
        public
        view
        returns (string[] memory)
    {
        uint256 count = 0;
        for (uint256 i = 0; i < emailAndDocumentHashs.length; i++) {
            if (keccak256(abi.encodePacked(emailAndDocumentHashs[i].email)) == keccak256(abi.encodePacked(email))) {
                count++;
            }
        }
        string[] memory documentIds = new string[](count);
        uint256 j = 0;
        for (uint256 i = 0; i < emailAndDocumentHashs.length; i++) {
            if (keccak256(abi.encodePacked(emailAndDocumentHashs[i].email)) == keccak256(abi.encodePacked(email))) {
                documentIds[j] = emailAndDocumentHashs[i].documentHash;
                j++;
            }
        }
        return documentIds;
    }
    // A function to revoke a document
    function revokeDocument(string memory documentId) public isExist(documentId){
        delete documents[documentId];
    }
    // A function to store email and public key
    function storeEmailAndDocumentHash(string memory email, string memory publicKey) public {
        emailAndPublicKeys.push(emailAndPublicKey(email, publicKey));
    }
    // A function to retrieve public key from email
    function getPublicKey(string memory email) public view returns (string memory){
        for (uint256 i = 0; i < emailAndPublicKeys.length; i++) {
            if (keccak256(abi.encodePacked(emailAndPublicKeys[i].email)) == keccak256(abi.encodePacked(email))) {
                return emailAndPublicKeys[i].publicKey;
            }
        }
        return "";
    }
}