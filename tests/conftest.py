import pytest
from brownie import accounts, XVader, Ownable, TestToken


@pytest.fixture(scope="session")
def deployer(accounts):
    yield accounts[0]


@pytest.fixture(scope="session")
def users(accounts):
    yield [accounts[1], accounts[2]]


@pytest.fixture(scope="module")
def ownable(deployer):
    yield Ownable.deploy({"from": deployer})


@pytest.fixture(scope="module")
def xVader(deployer, vader):
    yield XVader.deploy(vader, {"from": deployer})


# test contracts
@pytest.fixture(scope="module")
def vader(deployer):
    yield TestToken.deploy("VADER", "VADER", {"from": deployer})
