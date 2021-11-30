import brownie
from brownie import ZERO_ADDRESS


def test_nominate_new_owner(ownable, deployer, users):
    user = users[0]

    with brownie.reverts("not owner"):
        ownable.nominateNewOwner(user, {"from": user})

    tx = ownable.nominateNewOwner(user, {"from": deployer})

    assert ownable.owner() == deployer
    assert ownable.nominatedOwner() == user

    assert len(tx.events) == 1
    assert tx.events["OwnerNominated"].values() == [user]


def test_accept_ownership(ownable, deployer, users):
    user = users[0]

    with brownie.reverts("not nominated"):
        ownable.acceptOwnership({"from": deployer})

    tx = ownable.acceptOwnership({"from": user})

    assert ownable.owner() == user
    assert ownable.nominatedOwner() == ZERO_ADDRESS

    assert len(tx.events) == 1
    assert tx.events["OwnerChanged"].values() == [user]
