// SPDX-License-Identifier: MIT
pragma solidity 0.8.9;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Votes.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "./Ownable.sol";

contract XVader is ERC20Votes, ReentrancyGuard, Ownable {
    event SetMinStakeDuration(uint duration);

    // Address of vader token
    IERC20 public immutable vader;

    // Minimum time staked before unstake can be called
    uint public minStakeDuration;

    // Mapping from staker to timestamp of last stake
    mapping(address => uint) public lastStakedAt;

    /*
     * @dev Initializes contract's state by setting vader's tokens address and
     * setting current token's name and symbol.
     **/
    constructor(IERC20 _vader, uint _minStakeDuration)
        ERC20Permit("xVADER")
        ERC20("xVADER", "xVADER")
    {
        require(_vader != IERC20(address(0)), "vader = zero address");
        vader = _vader;
        _setMinStakeDuration(_minStakeDuration);
    }

    function _setMinStakeDuration(uint _minStakeDuration) private {
        require(_minStakeDuration > 0, "duration = 0");
        minStakeDuration = _minStakeDuration;
        emit SetMinStakeDuration(_minStakeDuration);
    }

    function setMinStakeDuration(uint _minStakeDuration) external onlyOwner {
        _setMinStakeDuration(_minStakeDuration);
    }

    // Locks vader and mints xVader
    function enter(uint _amount) external nonReentrant {
        // NOTE: timestamp is reset for msg.sender
        lastStakedAt[msg.sender] = block.timestamp;

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
        require(
            block.timestamp >= lastStakedAt[msg.sender] + minStakeDuration,
            "time < min"
        );

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
        // skip amount = 0, mint, burn and transfer to self
        if (amount > 0 && from != address(0) && to != address(0) && from != to) {
            uint fromTimestamp = lastStakedAt[from];
            uint toTimestamp = lastStakedAt[to];

            if (toTimestamp > 0) {
                /*
                f = lastStakedAt[from]
                t = lastStakedAt[to]
                a = amount
                b = balance of from

                if f <= t
                    lastStakedAt[to] = t
                else
                    lastStakedAt[to] = (f - t) * a / b + t
                */
                if (fromTimestamp > toTimestamp) {
                    lastStakedAt[to] +=
                        ((fromTimestamp - toTimestamp) * amount) /
                        balanceOf(from);
                }
            } else {
                // same time stamp as enter()
                lastStakedAt[to] = block.timestamp;
            }
        }
    }
}
