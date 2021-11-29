import brownie
from brownie import Ownable, ZERO_ADDRESS


def test_constructor(deployer):
    ownable = Ownable.deploy({"from": deployer})
    assert ownable.owner() == deployer


def test_nominate_new_owner(ownable, deployer, user_1):
    with brownie.reverts("not owner"):
        ownable.nominateNewOwner(user_1, {"from": user_1})

    tx = ownable.nominateNewOwner(user_1, {"from": deployer})

    assert ownable.owner() == deployer
    assert ownable.nominatedOwner() == user_1

    assert len(tx.events) == 1
    assert tx.events["OwnerNominated"].values() == [user_1]


def test_accept_ownership(ownable, deployer, user_1):
    with brownie.reverts("not nominated"):
        ownable.acceptOwnership({"from": deployer})

    tx = ownable.acceptOwnership({"from": user_1})

    assert ownable.owner() == user_1
    assert ownable.nominatedOwner() == ZERO_ADDRESS

    assert len(tx.events) == 1
    assert tx.events["OwnerChanged"].values() == [user_1]
