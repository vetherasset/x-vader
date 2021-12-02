const { expect, BN } = require("./setup")
const { ZERO_ADDRESS } = require("./util")

let accounts
let admin
let user
let vader
let xVader

describe("XVader", () => {
    before(async () => {
        accounts = await ethers.getSigners()
        admin = accounts[0]
        user = accounts[1]

        const TestToken = await ethers.getContractFactory("TestToken")
        vader = await TestToken.deploy("Vader", "Vader")
        await vader.deployed()

        const XVader = await ethers.getContractFactory("XVader")
        xVader = await XVader.deploy(vader.address)
        await xVader.deployed()
    })

    const snapshot = async () => {
        return {
            vader: {
                xVader: await vader.balanceOf(xVader.address),
                user: await vader.balanceOf(user.address),
            },
            xVader: {
                totalSupply: await xVader.totalSupply(),
                user: await xVader.balanceOf(user.address),
            },
        }
    }

    it("constructor", async () => {
        expect(await xVader.vader()).to.equal(vader.address)
    })

    it("initialize", async () => {
        await xVader.connect(admin).initialize()
        expect(await xVader.owner()).to.equal(admin.address)
        expect(await xVader.name()).to.equal("xVADER")
        expect(await xVader.symbol()).to.equal("xVADER")
        expect(await xVader.decimals()).to.equal(18)

        await expect(xVader.initialize()).to.be.rejected
    })

    it("should enter", async () => {
        const amount = ethers.utils.parseUnits("1000", 18)

        await vader.mint(user.address, amount)
        await vader.connect(user).approve(xVader.address, amount)

        let _before
        let _after

        _before = await snapshot()
        await xVader.connect(user).enter(amount)
        _after = await snapshot()

        expect(_after.vader.user.toString()).to.equal(
            _before.vader.user.sub(amount).toString()
        )
        expect(_after.vader.xVader.toString()).to.equal(
            _before.vader.xVader.add(amount).toString()
        )
        expect(_after.xVader.totalSupply.toString()).to.equal(amount.toString())
        expect(_after.xVader.user.toString()).to.equal(amount.toString())

        // mint pro-rata
        await vader.mint(user.address, amount)
        await vader.connect(user).approve(xVader.address, amount)

        _before = await snapshot()
        await xVader.connect(user).enter(amount)
        _after = await snapshot()

        const inc = amount.mul(_before.xVader.totalSupply).div(_before.vader.xVader)
        const delta = _after.xVader.user.sub(_before.xVader.user)

        expect(delta.toString()).to.equal(inc.toString())
    })

    it("should leave", async () => {
        const shares = await xVader.balanceOf(user.address)

        let _before = await snapshot()
        await xVader.connect(user).leave(shares)
        let _after = await snapshot()

        expect(_after.vader.user.toString()).to.equal(
            _before.vader.user.add(_before.vader.xVader).toString()
        )
        expect(_after.vader.xVader.toString()).to.equal("0")
        expect(_after.xVader.totalSupply.toString()).to.equal("0")
        expect(_after.xVader.user.toString()).to.equal("0")
    })
})
