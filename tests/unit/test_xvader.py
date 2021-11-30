import brownie
from brownie import XVader, ZERO_ADDRESS


def test_constructor(deployer, vader, xVader):
    with brownie.reverts("vader = zero address"):
        XVader.deploy(ZERO_ADDRESS, {"from": deployer})

    assert xVader.owner() == deployer
    assert xVader.vader() == vader
    assert xVader.name() == "xVADER"
    assert xVader.symbol() == "xVADER"
    assert xVader.decimals() == 18


def test_enter(vader, xVader, users):
    user = users[0]

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

    # mint pro-rata
    vader.mint(user, 1000 * 1e18)
    vader.approve(xVader, amount, {"from": user})

    xVader.enter(500 * 1e18, {"from": user})

    before = snapshot()
    tx = xVader.enter(500 * 1e18, {"from": user})
    after = snapshot()

    # rounding error from float
    error = 1e5
    expected_increase = (
        500 * 1e18 * before["xVader"]["totalSupply"] / before["vader"]["xVader"]
    )

    assert (
        abs(after["xVader"]["user"] - (before["xVader"]["user"] + expected_increase))
        <= error
    )


def test_leave(vader, xVader, users):
    user = users[0]

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
