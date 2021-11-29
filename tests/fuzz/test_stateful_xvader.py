import brownie
from brownie.test import strategy


MIN_STAKE_DURATION = 10


class StateMachine:
    # either user 0 or 1
    user_index = strategy("uint256", min_value=0, max_value=1)
    amount = strategy("uint256", max_value=1000)
    shares = strategy("uint256", min_value=1)
    # time elapsed
    dt = strategy("uint256", min_value=0, max_value=20)

    def __init__(cls, chain, xVader, vader, users):
        cls.chain = chain
        cls.xVader = xVader
        cls.vader = vader
        cls.users = users

    def setup(self):
        self.lastStakedAt = {}
        self.lastStakedAt[self.users[0]] = 0
        self.lastStakedAt[self.users[1]] = 0

    def rule_enter(self, user_index, amount):
        user = self.users[user_index]
        _amount = min(amount, self.vader.balanceOf(user))
        tx = self.xVader.enter(_amount, {"from": user})

        print("enter", "user", user_index, "amount", _amount)

        self.lastStakedAt[user.address] = tx.timestamp

    def rule_leave(self, user_index, shares, dt):
        if self.xVader.totalSupply() == 0:
            return

        self.chain.sleep(dt)

        user = self.users[user_index]
        _shares = min(shares, self.xVader.balanceOf(user))

        if _shares == 0:
            return

        print(
            "leave",
            "user",
            user_index,
            "shares",
            _shares,
            self.chain.time() >= self.lastStakedAt[user] + MIN_STAKE_DURATION,
        )

        if self.chain.time() >= self.lastStakedAt[user] + MIN_STAKE_DURATION:
            self.xVader.leave(_shares, {"from": user})
        else:
            print("Can't leave")
            with brownie.reverts("time < min"):
                self.xVader.leave(_shares, {"from": user})

    def invariant(self):
        # no invariants, just checking enter / leave
        pass


def test_stateful(state_machine, chain, xVader, vader, users):
    vader.mint(users[0], 2 ** 255 - 1)
    vader.mint(users[1], 2 ** 255 - 1)

    vader.approve(xVader, 2 ** 256 - 1, {"from": users[0]})
    vader.approve(xVader, 2 ** 256 - 1, {"from": users[1]})

    state_machine(StateMachine, chain, xVader, vader, users)
