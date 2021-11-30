// SPDX-License-Identifier: MIT
pragma solidity 0.8.9;

import "../Ownable.sol";

contract TestOwnable is Ownable {
    constructor() {
        owner = msg.sender;
    }
}
