import brownie
from brownie import XVader, ZERO_ADDRESS


def test_constructor(deployer, vader, xVader):
    with brownie.reverts("vader = zero address"):
        min_stake_duration = 10
        XVader.deploy(ZERO_ADDRESS, min_stake_duration, {"from": deployer})

    with brownie.reverts("min stake duration = 0"):
        XVader.deploy(vader, 0, {"from": deployer})

    assert xVader.vader() == vader
    assert xVader.MIN_STAKE_DURATION() > 0
    assert xVader.name() == "xVADER"
    assert xVader.symbol() == "xVADER"
    assert xVader.decimals() == 18


def test_enter(vader, xVader, user):
    # mint 1:1 xVader:Vader when xVader or Vader = 0
    amount = 1000 * 1e18
    vader.mint(user, amount)
    vader.approve(xVader, amount, {"from": user})

    def snapshot():
        return {
            "vader": {
                "xVader": vader.balanceOf(xVader),
                "user": vader.balanceOf(user),
            },
            "xVader": {
                "totalSupply": xVader.totalSupply(),
                "user": xVader.balanceOf(user),
            },
        }

    before = snapshot()
    tx = xVader.enter(amount, {"from": user})
    after = snapshot()

    assert after["vader"]["user"] == before["vader"]["user"] - amount
    assert after["vader"]["xVader"] == before["vader"]["xVader"] + amount
    assert after["xVader"]["totalSupply"] == amount
    assert after["xVader"]["user"] == amount
    assert xVader.lastStakedAt(user) == tx.timestamp

    # mint pro-rata
    vader.mint(user, 1000 * 1e18)
    vader.approve(xVader, amount, {"from": user})

    xVader.enter(500 * 1e18, {"from": user})

    before = snapshot()
    tx = xVader.enter(500 * 1e18, {"from": user})
    after = snapshot()

    assert xVader.lastStakedAt(user) == tx.timestamp

    # rounding error from float
    error = 1e5
    expected_increase = (
        500 * 1e18 * before["xVader"]["totalSupply"] / before["vader"]["xVader"]
    )

    assert (
        abs(after["xVader"]["user"] - (before["xVader"]["user"] + expected_increase))
        <= error
    )


def test_leave(chain, vader, xVader, user):
    with brownie.reverts("time < min"):
        xVader.leave(1, {"from": user})

    last_staked_at = xVader.lastStakedAt(user)
    min_stake_duration = xVader.MIN_STAKE_DURATION()
    duration = last_staked_at + min_stake_duration

    chain.sleep(duration)

    def snapshot():
        return {
            "vader": {
                "xVader": vader.balanceOf(xVader),
                "user": vader.balanceOf(user),
            },
            "xVader": {
                "totalSupply": xVader.totalSupply(),
                "user": xVader.balanceOf(user),
            },
        }

    shares = xVader.balanceOf(user)

    before = snapshot()
    xVader.leave(shares, {"from": user})
    after = snapshot()

    assert after["vader"]["user"] == before["vader"]["user"] + before["vader"]["xVader"]
    assert after["vader"]["xVader"] == 0
    assert after["xVader"]["totalSupply"] == 0
    assert after["xVader"]["user"] == 0
