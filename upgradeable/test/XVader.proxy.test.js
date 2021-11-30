const { expect } = require("./setup")

let accounts
let vader
let xVader

describe("XVader (proxy)", function () {
  beforeEach(async function () {
    accounts = await ethers.getSigners()

    const Vader = await ethers.getContractFactory("TestToken")
    vader = await Vader.deploy("VADER", "VADER")
    await vader.deployed()

    const XVader = await ethers.getContractFactory("XVader")
    xVader = await upgrades.deployProxy(XVader, [vader.address], {
      initializer: "initialize",
    })
  })

  it("should initialize", async function () {
    expect(await xVader.vader()).to.equal(vader.address)
    expect(await xVader.owner()).to.equal(accounts[0].address)
    expect(await xVader.name()).to.equal("xVADER")
    expect(await xVader.symbol()).to.equal("xVADER")
    expect(await xVader.decimals()).to.equal(18)

    await expect(xVader.initialize(vader.address)).to.be.rejected
  })
})
