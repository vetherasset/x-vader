const { expect } = require("./setup")
const { ZERO_ADDRESS } = require("./util")

let accounts
let admin
let user
let ownable

describe("Ownable", () => {
    before(async () => {
        accounts = await ethers.getSigners()
        admin = accounts[0]
        user = accounts[1]

        const TestOwnable = await ethers.getContractFactory("TestOwnable")
        ownable = await TestOwnable.connect(admin).deploy()
        await ownable.deployed()
    })

    it("constructor", async () => {
        expect(await ownable.owner()).to.equal(admin.address)
        expect(await ownable.nominatedOwner()).to.equal(ZERO_ADDRESS)
    })

    it("should nominate new owner", async () => {
        await expect(
            ownable.connect(user).nominateNewOwner(user.address)
        ).to.be.rejectedWith("not owner")

        await ownable.connect(admin).nominateNewOwner(user.address)

        expect(await ownable.nominatedOwner()).to.equal(user.address)
    })

    it("should accept new owner", async () => {
        await expect(ownable.connect(admin).acceptOwnership()).to.be.rejectedWith(
            "not nominated"
        )

        await ownable.connect(user).acceptOwnership()

        expect(await ownable.owner()).to.equal(user.address)
        expect(await ownable.nominatedOwner()).to.equal(ZERO_ADDRESS)
    })
})
