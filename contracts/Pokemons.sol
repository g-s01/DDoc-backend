// SPDX-License-Identifier: MIT
pragma solidity ^0.8.2;
import "./ERC.sol";

/**
* @title Pokemons
* @dev The contract is an ERC token that represents a Pokemon
 */
contract Pokemons is ERC {
    string public name;
    string public symbol;
    // tokenId => pokemon
    uint256 public tokencount;
    mapping(uint256 => string) private _tokenURIs;

    constructor(string memory _name, string memory _symbol) {
        name = _name;
        symbol = _symbol;
    }
    function tokenURI(address to, uint256 tokenId) public view returns(string memory) {
        require(_owners[tokenId] == to, "Address is not the owner");
        return _tokenURIs[tokenId];
    }
    function mint(string memory _tokenURI) public {
        tokencount++;
       _balances[msg.sender]++;
         _owners[tokencount] = msg.sender;
        _tokenURIs[tokencount] = _tokenURI;
        emit Transfer(address(0), msg.sender, tokencount);
    }

    function supportsInterface(bytes4 interfaceId) public pure override returns (bool) {
        return interfaceId == 0x01ffc9a7 || interfaceId == 0x80ac58cd || interfaceId == 0x5b5e139f;
    }
    
}