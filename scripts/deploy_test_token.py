from brownie import TestToken, accounts, network


def main():
    account = accounts.load("dev")

    net = network.show_active()
    assert net == "kovan"

    TestToken.deploy("test token", "TEST", {"from": account}, publish_source=True)
