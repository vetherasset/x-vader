// SPDX-License-Identifier: MIT AND AGPL-3.0-or-later
pragma solidity 0.8.9;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract TestToken is ERC20 {
    // decimals = 18
    constructor(string memory name, string memory symbol) ERC20(name, symbol) {}

    function mint(address _to, uint _amount) external {
        _mint(_to, _amount);
    }

    function burn(address _from, uint _amount) external {
        _burn(_from, _amount);
    }
}
