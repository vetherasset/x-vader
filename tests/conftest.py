import pytest
from brownie import accounts, XVader, TestToken


@pytest.fixture(scope="session")
def deployer(accounts):
    yield accounts[0]


@pytest.fixture(scope="session")
def user(accounts):
    yield accounts[1]


@pytest.fixture(scope="module")
def xVader(deployer, vader):
    yield XVader.deploy(vader, {"from": deployer})


# test contracts
@pytest.fixture(scope="module")
def vader(deployer):
    yield TestToken.deploy("VADER", "VADER", {"from": deployer})
