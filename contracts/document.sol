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
        bytes ipfsHashSigned;
        string orgEmail;
    }
    struct emailAndDocumentHashAndOrgEmail{
        string email;
        bytes documentHash;
        string orgEmail;
    }
    struct emailAndPublicKey{
        string email;
        bytes publicKey;
    }
    // TODO: Comment THIS in the final doc
    struct emailAndPrivateKey{
        string email;
        bytes privateKey;
    }
    struct DocumentHashAndOrgEmail{
        bytes documentHash;
        string orgEmail;
    }
    emailAndPublicKey[] public emailAndPublicKeys;
    emailAndPrivateKey[] public emailAndPrivateKeys;
    emailAndDocumentHashAndOrgEmail[] public emailAndDocumentHashAndOrgEmails;
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
        string memory recipientEmail,
        bytes memory ipfsHashSigned,
        string memory orgEmail
    ) public isOriginal (documentId){
        Document memory newDocument = Document(
            recipientEmail,
            ipfsHashSigned,
            orgEmail
        );
        documents[documentId] = newDocument;
        emailAndDocumentHashAndOrgEmails.push(emailAndDocumentHashAndOrgEmail(recipientEmail, ipfsHashSigned, orgEmail));
        emit documentIssued(recipientEmail, ipfsHashSigned, orgEmail);
    }
    // A function to get certificates for a particular email
    function getDocument(string memory email)
        public
        view
        returns (DocumentHashAndOrgEmail[] memory)
    {
        uint256 count = 0;
        for (uint256 i = 0; i < emailAndDocumentHashAndOrgEmails.length; i++) {
            if (keccak256(abi.encodePacked(emailAndDocumentHashAndOrgEmails[i].email)) == keccak256(abi.encodePacked(email))) {
                count++;
            }
        }
        DocumentHashAndOrgEmail[] memory documentIds = new DocumentHashAndOrgEmail[](count);
        uint256 j = 0;
        for (uint256 i = 0; i < emailAndDocumentHashAndOrgEmails.length; i++) {
            if (keccak256(abi.encodePacked(emailAndDocumentHashAndOrgEmails[i].email)) == keccak256(abi.encodePacked(email))) {
                documentIds[j] = DocumentHashAndOrgEmail(emailAndDocumentHashAndOrgEmails[i].documentHash, emailAndDocumentHashAndOrgEmails[i].orgEmail);
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
    function storeEmailAndPublicKey(string memory email, bytes memory publicKey) public {
        emailAndPublicKeys.push(emailAndPublicKey(email, publicKey));
    }
    // A function to retrieve public key from email
    function getPublicKey(string memory email) public view returns (bytes memory){
        for (uint256 i = 0; i < emailAndPublicKeys.length; i++) {
            if (keccak256(abi.encodePacked(emailAndPublicKeys[i].email)) == keccak256(abi.encodePacked(email))) {
                return emailAndPublicKeys[i].publicKey;
            }
        }
        return "";
    }
    // A function to store email and private key
    function storeEmailAndPrivateKey(string memory email, bytes memory privateKey) public {
        emailAndPrivateKeys.push(emailAndPrivateKey(email, privateKey));
    }
    // A function to retrieve private key from email
    function getPrivateKey(string memory email) public view returns (bytes memory){
        for (uint256 i = 0; i < emailAndPrivateKeys.length; i++) {
            if (keccak256(abi.encodePacked(emailAndPrivateKeys[i].email)) == keccak256(abi.encodePacked(email))) {
                return emailAndPrivateKeys[i].privateKey;
            }
        }
        return "";
    }
}