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

### Kovan

-   ProxyAdmin: [0x800eD5623AfaE464aabC957cAb9736D3817060a7](https://kovan.etherscan.io/address/0x800eD5623AfaE464aabC957cAb9736D3817060a7)
-   XVader (Proxy): [0xfD224C48F57deaCd0D8a5C3C4917eecE472Bb134](https://kovan.etherscan.io/address/0xfD224C48F57deaCd0D8a5C3C4917eecE472Bb134)
