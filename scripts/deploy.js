const assert = require("assert")
const hre = require("hardhat")
const { ethers, upgrades } = hre
const { VADER } = require("./constants")

async function main() {
    try {
        console.log(`network: ${hre.network.name}`)
        const vader = VADER[hre.network.name]
        assert(vader, "vader not defined")

        console.log(`vader: ${vader}`)

        const XVader = await ethers.getContractFactory("XVader")
        console.log("Deploying XVader...")
        const xVader = await upgrades.deployProxy(XVader, {
            initializer: "initialize",
            constructorArgs: [vader],
        })
        await xVader.deployed()
        console.log("XVader deployed to:", xVader.address)
    } catch (error) {
        console.error(error)
        process.exit(1)
    }
}

main()
