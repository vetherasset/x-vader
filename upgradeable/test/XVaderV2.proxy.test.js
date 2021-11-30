const { expect } = require("./setup")

let accounts
let vader
let xVader
let xVaderV2

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

    const XVaderV2 = await ethers.getContractFactory("XVaderV2")
    xVaderV2 = await upgrades.upgradeProxy(xVader.address, XVaderV2)
  })

  it("should initialize", async function () {
    expect(await xVaderV2.vader()).to.equal(await xVader.vader())
    expect(await xVaderV2.vader()).to.equal(vader.address)

    expect(await xVaderV2.owner()).to.equal(await xVader.owner())
    expect(await xVaderV2.owner()).to.equal(accounts[0].address)

    expect(await xVaderV2.name()).to.equal("xVADER")
    expect(await xVaderV2.symbol()).to.equal("xVADER")
    expect(await xVaderV2.decimals()).to.equal(18)

    await expect(xVaderV2.initialize(vader.address)).to.be.rejected
  })
})
