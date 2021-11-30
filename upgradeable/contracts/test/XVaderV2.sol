// SPDX-License-Identifier: MIT
pragma solidity 0.8.9;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC20/extensions/ERC20VotesUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/security/ReentrancyGuardUpgradeable.sol";
import "../Ownable.sol";

contract XVaderV2 is
    Initializable,
    ERC20VotesUpgradeable,
    ReentrancyGuardUpgradeable,
    Ownable
{
    // Address of vader token
    IERC20 public vader;

    // used for testing upgrade
    uint public version;

    function test() external onlyOwner {
        version += 1;
    }

    /*
    TODO: questions
    - function order matters?
    - init is not called on v2?
    */

    // TODO: remove constructor

    function initialize(IERC20 _vader) external initializer {
        require(_vader != IERC20(address(0)), "vader = zero address");
        vader = _vader;

        owner = msg.sender;

        __ReentrancyGuard_init();
        __ERC20_init("xVADER", "xVADER");
        __ERC20Permit_init("xVADER");

        version = 2;
    }

    // Locks vader and mints xVader
    function enter(uint _amount) external nonReentrant {
        // Gets the amount of vader locked in the contract
        uint totalVader = vader.balanceOf(address(this));
        // Gets the amount of xVader in existence
        uint totalShares = totalSupply();

        // If no xVader exists, mint it 1:1 to the amount put in.
        // Calculate and mint the amount of xVader the vader is worth.
        // The ratio will change overtime, as xVader is burned/minted and
        // vader deposited + gained from fees / withdrawn.
        uint xVADERToMint = totalShares == 0 || totalVader == 0
            ? _amount
            : (_amount * totalShares) / totalVader;

        _mint(msg.sender, xVADERToMint);

        // Lock the vader in the contract
        vader.transferFrom(msg.sender, address(this), _amount);
    }

    // Claim back your VADER
    // Unlocks the staked + gained vader and burns xVader
    function leave(uint _shares) external nonReentrant {
        // Calculates the amount of vader the xVader is worth
        uint vaderAmount = (_shares * vader.balanceOf(address(this))) / totalSupply();

        _burn(msg.sender, _shares);
        vader.transfer(msg.sender, vaderAmount);
    }
}