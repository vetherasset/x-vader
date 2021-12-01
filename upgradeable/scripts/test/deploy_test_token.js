const assert = require("assert")
const hre = require("hardhat")
const { ethers } = hre

async function main() {
    try {
        console.log(`network: ${hre.network.name}`)
        assert(hre.network.name == "kovan")

        const TestToken = await ethers.getContractFactory("TestToken")
        const testToken = await TestToken.deploy("test", "TEST")
        testToken.deployed()

        console.log(`TestToken: ${testToken.address}`)
    } catch (error) {
        console.error(error)
        process.exit(1)
    }
}

main()
