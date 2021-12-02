const { expect } = require("../setup")

let accounts
let admin
let user
let vader
let xVader
let xVaderV2

describe("XVader V2 proxy", () => {
    before(async () => {
        accounts = await ethers.getSigners()
        admin = accounts[0]
        user = accounts[0]

        const Vader = await ethers.getContractFactory("TestToken")
        vader = await Vader.deploy("VADER", "VADER")
        await vader.deployed()

        const XVader = await ethers.getContractFactory("XVader")
        xVader = await upgrades.deployProxy(XVader, {
            initializer: "initialize",
            constructorArgs: [vader.address],
        })
    })

    it("should upgrade", async () => {
        // xVader is initialized
        expect(await xVader.vader()).to.equal(vader.address)
        expect(await xVader.owner()).to.equal(admin.address)

        // cannot re-initialize xVader
        await expect(xVader.initialize()).to.be.rejected

        // enter
        const amount = ethers.utils.parseUnits("1000", 18)
        const ZERO = ethers.utils.parseUnits("0", 18)

        await vader.mint(user.address, amount)
        await vader.connect(user).approve(xVader.address, amount)

        await xVader.connect(user).enter(amount)

        // upgrade
        const XVaderV2 = await ethers.getContractFactory("XVaderV2")
        xVaderV2 = await upgrades.upgradeProxy(xVader.address, XVaderV2, {
            constructorArgs: [vader.address],
        })

        expect(await xVaderV2.vader()).to.equal(vader.address)
        expect(await xVaderV2.owner()).to.equal(admin.address)

        // test shares
        let shares = await xVaderV2.balanceOf(user.address)
        expect(shares.gt(ZERO)).to.eq(true)

        await xVader.connect(user).leave(shares)

        shares = await xVaderV2.balanceOf(user.address)
        expect(shares.toString()).to.eq("0")
    })
})
