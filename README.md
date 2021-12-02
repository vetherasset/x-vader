# XVader

### Install

```shell
npm i
cp secrets.sample.json secrets.json
```

### Dev

```shell
npx hardhat compile

npx hardhat test
```

### Deploy

```shell
# clean build
npx hardhat clean
npx hardhat compile

# deploy
npx hardhat run --network kovan scripts/deploy.js

# verify
npx hardhat verify --network kovan DEPLOYED_CONTRACT_ADDRESS "Constructor argument 1"

# upgrade
npx hardhat run --network kovan scripts/test/upgrade.js
```

### Mainnet

-   ProxyAdmin: [0x888939b157032189D667577D4e5A3C93c1B1FdC7](https://kovan.etherscan.io/address/0x888939b157032189D667577D4e5A3C93c1B1FdC7)
-   XVader (Proxy): [0x665ff8fAA06986Bd6f1802fA6C1D2e7d780a7369](https://kovan.etherscan.io/address/0x665ff8fAA06986Bd6f1802fA6C1D2e7d780a7369)

### Kovan

-   ProxyAdmin: [0x800eD5623AfaE464aabC957cAb9736D3817060a7](https://kovan.etherscan.io/address/0x800eD5623AfaE464aabC957cAb9736D3817060a7)
-   XVader (Proxy): [0xfD224C48F57deaCd0D8a5C3C4917eecE472Bb134](https://kovan.etherscan.io/address/0xfD224C48F57deaCd0D8a5C3C4917eecE472Bb134)
