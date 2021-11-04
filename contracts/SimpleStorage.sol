// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    // get initialized to 0
    uint256 public favuoriteNumber;

    function store(uint256 _favoriteNumber) public returns (uint256) {
        favuoriteNumber = _favoriteNumber;
        return _favoriteNumber;
    }

    function retrieve() public view returns (uint256) {
        return favuoriteNumber;
    }

    struct People {
        uint256 favuoriteNumber;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public nameToFavouriteNumber;

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People({favuoriteNumber: _favoriteNumber, name: _name}));
        nameToFavouriteNumber[_name] = _favoriteNumber;
    }
}
