from brownie import XVader, accounts, network

config = {
    "mainnet": {"vader": ""},
    "kovan": {"vader": "0x237E9d2F4d4834fD3fCB0ECdeE912682F5D24984"},
}


def main():
    account = accounts.load("dev")

    net = network.show_active()
    assert net == "kovan"

    vader = config[net]["vader"]

    XVader.deploy(vader, {"from": account}, publish_source=True)
