// SPDX-License-Identifier: MIT
pragma solidity 0.8.9;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC20/extensions/ERC20VotesUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/security/ReentrancyGuardUpgradeable.sol";
import "./Ownable.sol";

contract XVaderV2 is
    Initializable,
    ERC20VotesUpgradeable,
    ReentrancyGuardUpgradeable,
    Ownable
{
    event SetStakeDuration(uint duration);

    /// @custom:oz-upgrades-unsafe-allow state-variable-immutable
    IERC20 public immutable vader;

    // Minimum time staked before unstake can be called
    uint public stakeDuration;

    // Mapping from staker to timestamp of last stake
    mapping(address => uint) public stakedAt;

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor(IERC20 _vader) initializer {
        require(_vader != IERC20(address(0)), "vader = zero address");
        vader = _vader;
    }

    function setStakeDuration(uint _stakeDuration) external onlyOwner {
        require(_stakeDuration > 0, "duration = 0");
        stakeDuration = _stakeDuration;
        emit SetStakeDuration(_stakeDuration);
    }

    // Locks vader and mints xVader
    function enter(uint _amount) external nonReentrant {
        // NOTE: timestamp is reset for msg.sender
        stakedAt[msg.sender] = block.timestamp;

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
        require(block.timestamp >= stakedAt[msg.sender] + stakeDuration, "time < min");

        // Calculates the amount of vader the xVader is worth
        uint vaderAmount = (_shares * vader.balanceOf(address(this))) / totalSupply();

        _burn(msg.sender, _shares);
        vader.transfer(msg.sender, vaderAmount);
    }

    function _beforeTokenTransfer(
        address from,
        address to,
        uint amount
    ) internal override {
        // skip if amount = 0, mint, burn or transfer to self
        if (amount == 0 || from == address(0) || to == address(0) || from == to) {
            return;
        }

        uint fromTimestamp = stakedAt[from];
        // timestamp may be 0 from V1 implementation
        if (fromTimestamp > 0) {
            /*
            f = stakedAt[from]
            t = stakedAt[to]
            a = amount
            b = balance of to

            if f > t
                stakedAt[to] = (a * f + b + t) / (a + b)
            else
                stakedAt[to] = t
            */
            uint toTimestamp = stakedAt[to];
            if (fromTimestamp > toTimestamp) {
                uint toBal = balanceOf(to);
                stakedAt[to] =
                    (amount * fromTimestamp + toBal * toTimestamp) /
                    (amount + toBal);
            }
        } else {
            stakedAt[to] = block.timestamp;
        }
    }
}
