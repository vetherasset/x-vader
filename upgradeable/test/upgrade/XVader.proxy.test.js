const { expect } = require("../setup")

let accounts
let admin
let user
let vader
let xVader

describe("XVader proxy", () => {
    before(async () => {
        accounts = await ethers.getSigners()
        admin = accounts[0]
        user = accounts[1]

        const Vader = await ethers.getContractFactory("TestToken")
        vader = await Vader.deploy("VADER", "VADER")
        await vader.deployed()

        const XVader = await ethers.getContractFactory("XVader")
        xVader = await upgrades.deployProxy(XVader, {
            initializer: "initialize",
            constructorArgs: [vader.address],
        })
    })

    it("should initialize", async () => {
        expect(await xVader.vader()).to.equal(vader.address)
        expect(await xVader.owner()).to.equal(admin.address)
        expect(await xVader.name()).to.equal("xVADER")
        expect(await xVader.symbol()).to.equal("xVADER")
        expect(await xVader.decimals()).to.equal(18)

        await expect(xVader.initialize(vader.address)).to.be.rejected
    })

    it("should enter and leave", async () => {
        const amount = ethers.utils.parseUnits("1000", 18)
        const ZERO = ethers.utils.parseUnits("0", 18)

        await vader.mint(user.address, amount)
        await vader.connect(user).approve(xVader.address, amount)

        await xVader.connect(user).enter(amount)

        let shares = await xVader.balanceOf(user.address)
        expect(shares.gt(ZERO)).to.eq(true)

        await xVader.connect(user).leave(shares)

        shares = await xVader.balanceOf(user.address)
        expect(shares.toString()).to.eq("0")
    })
})
