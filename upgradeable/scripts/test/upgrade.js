const assert = require("assert")
const hre = require("hardhat")
const { ethers, upgrades } = hre
const { VADER, XVADER } = require("../constants")

async function main() {
    try {
        console.log(`network: ${hre.network.name}`)

        const vader = VADER[hre.network.name]
        assert(vader, "vader not defined")
        const xVader = XVADER[hre.network.name]
        assert(xVader, "xVader not defined")

        console.log(`vader: ${vader}`)
        console.log(`xVader: ${xVader}`)

        const XVaderV2 = await ethers.getContractFactory("XVaderV2")
        console.log("Upgrading XVader...")
        const xVaderV2 = await upgrades.upgradeProxy(xVader, XVaderV2, {
            constructorArgs: [vader],
        })
        xVaderV2.deployed()

        console.log("XVader upgraded")
    } catch (error) {
        console.error(error)
        process.exit(1)
    }
}

main()
