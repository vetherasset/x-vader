# X Vader

### Install

```shell
# install virtualenv
python3 -m pip install --user virtualenv
virtualenv -p python3 venv
source venv/bin/activate

pip install eth-brownie

brownie pm install OpenZeppelin/openzeppelin-contracts@4.3.2
brownie pm install OpenZeppelin/openzeppelin-contracts-upgradeable@4.3.2

npm i

cp .env.sample .env
```

### Development

```shell
brownie compile
```

### Test

```shell
brownie test tests/path-to-test-file-or-folder -s
```

#### Deploy

```shell
brownie run scripts/deploy_test_token.py --network kovan
```

### Misc

```shell
# select solc compiler
solc-select install 0.8.9
solc-select use 0.8.9

# check code size (max 2457 bytes)
brownie compile -s
```
