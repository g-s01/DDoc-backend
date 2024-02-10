// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.9;

/// Contract DEPLOYED on SEPOLIA Network: 0x04b3AdDF4e17e5f3af108456785a1450eE5Aa18C

/// @title A contract to issue/get/revoke documents to anyone
/// @author g-s01
/// @notice A contract to issue/get/revoke documents to anyone
/// @dev Verification of the document is not implemented, and has been done in the frontend
contract Record{
    // A document can be uniquely identified by the recipient's email,
    // the hash of the document on IPFS
    // and the email of the organization that issued the document
    struct Document{
        string documentName;
        string recipientEmail;
        bytes ipfsHashSigned;
        string orgEmail;
    }
    struct recipientEmailAndDocumentNameAndDocumentHashAndOrgEmail{
        string recipientEmail;
        string documentName;
        bytes documentHash;
        string orgEmail;
    }
    struct recipientEmailAndPublicKey{
        string recipientEmail;
        bytes publicKey;
    }
    struct DocumentHashAndDocumentNameAndOrgEmail{
        bytes documentHash;
        string documentName;
        string orgEmail;
    }
    // An array of email and public keys
    recipientEmailAndPublicKey[] public recipientEmailAndPublicKeys;
    // An array of email and document hash and organization email
    recipientEmailAndDocumentNameAndDocumentHashAndOrgEmail[] public recipientEmailAndDocumentNameAndDocumentHashAndOrgEmails;
    // A mapping from the document ID to the document
    mapping(string => Document) public documents;
    // An event that is emitted when a document is issued
    event documentIssued(string recipientEmail, bytes ipfsHashSigned, string orgEmail);
    // Modifier to check whether the certificate is original or not
    modifier isOriginal(string memory documentId){
        require(
            bytes(documents[documentId].ipfsHashSigned).length == 0,
            "This document is not original"
        );
        _;
    }
    // Modifier to check whether the certificate exists or not
    modifier isExist(string memory documentId){
        require(
            bytes(documents[documentId].ipfsHashSigned).length != 0,
            "This document does not exist"
        );
        _;
    }
    // A function to issue a document
    function issueDocument(
        string memory documentId,
        string memory documentName,
        string memory recipientEmail,
        bytes memory ipfsHashSigned,
        string memory orgEmail
    ) public isOriginal (documentId){
        Document memory newDocument = Document(
            documentName,
            recipientEmail,
            ipfsHashSigned,
            orgEmail
        );
        documents[documentId] = newDocument;
        recipientEmailAndDocumentNameAndDocumentHashAndOrgEmails.push(recipientEmailAndDocumentNameAndDocumentHashAndOrgEmail(recipientEmail, documentName, ipfsHashSigned, orgEmail));
        emit documentIssued(recipientEmail, ipfsHashSigned, orgEmail);
    }
    // A function to get certificates for a particular email
    function getDocument(string memory email)
        public
        view
        returns (DocumentHashAndDocumentNameAndOrgEmail[] memory)
    {
        uint256 count = 0;
        for (uint256 i = 0; i < recipientEmailAndDocumentNameAndDocumentHashAndOrgEmails.length; i++) {
            if (keccak256(abi.encodePacked(recipientEmailAndDocumentNameAndDocumentHashAndOrgEmails[i].recipientEmail)) == keccak256(abi.encodePacked(email))) {
                count++;
            }
        }
        DocumentHashAndDocumentNameAndOrgEmail[] memory documentIds = new DocumentHashAndDocumentNameAndOrgEmail[](count);
        uint256 j = 0;
        for (uint256 i = 0; i < recipientEmailAndDocumentNameAndDocumentHashAndOrgEmails.length; i++) {
            if (keccak256(abi.encodePacked(recipientEmailAndDocumentNameAndDocumentHashAndOrgEmails[i].recipientEmail)) == keccak256(abi.encodePacked(email))) {
                documentIds[j] = DocumentHashAndDocumentNameAndOrgEmail(recipientEmailAndDocumentNameAndDocumentHashAndOrgEmails[i].documentHash,recipientEmailAndDocumentNameAndDocumentHashAndOrgEmails[i].documentName,recipientEmailAndDocumentNameAndDocumentHashAndOrgEmails[i].orgEmail);
                j++;
            }
        }
        return documentIds;
    }
    // A function to revoke a document
    function revokeDocument(string memory documentId) public isExist(documentId){
        documents[documentId].ipfsHashSigned = "";
    }
    // A function to store email and public key
    function storeEmailAndPublicKey(string memory email, bytes memory publicKey) public {
        recipientEmailAndPublicKeys.push(recipientEmailAndPublicKey(email, publicKey));
    }
    // A function to retrieve public key from email
    function getPublicKey(string memory email) public view returns (bytes memory){
        for (uint256 i = 0; i < recipientEmailAndPublicKeys.length; i++) {
            if (keccak256(abi.encodePacked(recipientEmailAndPublicKeys[i].recipientEmail)) == keccak256(abi.encodePacked(email))) {
                return recipientEmailAndPublicKeys[i].publicKey;
            }
        }
        return "";
    }
    // A function to see whether a document exists or not
    function isDocumentExist(string memory documentId) public view returns (bool){
        if (bytes(documents[documentId].ipfsHashSigned).length != 0) {
            return true;
        }
        return false;
    }
}