import brownie
from brownie import XVader, ZERO_ADDRESS


def test_constructor(deployer, vader, xVader):
    with brownie.reverts("vader = zero address"):
        min_stake_duration = 10
        XVader.deploy(ZERO_ADDRESS, min_stake_duration, {"from": deployer})

    with brownie.reverts("min stake duration = 0"):
        XVader.deploy(vader, 0, {"from": deployer})

    assert xVader.owner() == deployer
    assert xVader.vader() == vader
    assert xVader.minStakeDuration() > 0
    assert xVader.name() == "xVADER"
    assert xVader.symbol() == "xVADER"
    assert xVader.decimals() == 18


def test_set_min_stake_duration(deployer, user_1, xVader):
    with brownie.reverts("not owner"):
        xVader.setMinStakeDuration(1, {"from": user_1})

    with brownie.reverts("min stake duration = 0"):
        xVader.setMinStakeDuration(0, {"from": deployer})

    tx = xVader.setMinStakeDuration(11, {"from": deployer})

    assert xVader.minStakeDuration() == 11
    assert tx.events["SetMinStakeDuration"].values() == [11]


def test_enter(vader, xVader, user_1):
    # mint 1:1 xVader:Vader when xVader or Vader = 0
    amount = 1000 * 1e18
    vader.mint(user_1, amount)
    vader.approve(xVader, amount, {"from": user_1})

    def snapshot():
        return {
            "vader": {
                "xVader": vader.balanceOf(xVader),
                "user_1": vader.balanceOf(user_1),
            },
            "xVader": {
                "totalSupply": xVader.totalSupply(),
                "user_1": xVader.balanceOf(user_1),
            },
        }

    before = snapshot()
    tx = xVader.enter(amount, {"from": user_1})
    after = snapshot()

    assert after["vader"]["user_1"] == before["vader"]["user_1"] - amount
    assert after["vader"]["xVader"] == before["vader"]["xVader"] + amount
    assert after["xVader"]["totalSupply"] == amount
    assert after["xVader"]["user_1"] == amount
    assert xVader.lastStakedAt(user_1) == tx.timestamp

    # mint pro-rata
    vader.mint(user_1, 1000 * 1e18)
    vader.approve(xVader, amount, {"from": user_1})

    xVader.enter(500 * 1e18, {"from": user_1})

    before = snapshot()
    tx = xVader.enter(500 * 1e18, {"from": user_1})
    after = snapshot()

    assert xVader.lastStakedAt(user_1) == tx.timestamp

    # rounding error from float
    error = 1e5
    expected_increase = (
        500 * 1e18 * before["xVader"]["totalSupply"] / before["vader"]["xVader"]
    )

    assert (
        abs(
            after["xVader"]["user_1"] - (before["xVader"]["user_1"] + expected_increase)
        )
        <= error
    )


def test_leave(chain, vader, xVader, user_1):
    with brownie.reverts("time < min"):
        xVader.leave(1, {"from": user_1})

    last_staked_at = xVader.lastStakedAt(user_1)
    min_stake_duration = xVader.minStakeDuration()
    duration = last_staked_at + min_stake_duration

    chain.sleep(duration)

    def snapshot():
        return {
            "vader": {
                "xVader": vader.balanceOf(xVader),
                "user_1": vader.balanceOf(user_1),
            },
            "xVader": {
                "totalSupply": xVader.totalSupply(),
                "user_1": xVader.balanceOf(user_1),
            },
        }

    shares = xVader.balanceOf(user_1)

    before = snapshot()
    xVader.leave(shares, {"from": user_1})
    after = snapshot()

    assert (
        after["vader"]["user_1"]
        == before["vader"]["user_1"] + before["vader"]["xVader"]
    )
    assert after["vader"]["xVader"] == 0
    assert after["xVader"]["totalSupply"] == 0
    assert after["xVader"]["user_1"] == 0
