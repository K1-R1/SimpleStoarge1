from solcx import compile_standard, install_solc
from web3 import Web3
import json

with open('./SimpleStorage.sol', 'r') as file:
    simple_storage_file = file.read()
    
#complile
install_solc('0.8.0')
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version='0.8.0',
)

with open('compiled_code.json','w') as file:
    json.dump(compiled_sol, file)

#deploy

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connecting to ganache
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
chain_id = 5777
my_address = '0xA56810ba872c6910883860E98992986fc3140664'
private_key = '0x61d42a5f3aa6e850e9d889d75f3466ddb105d9267ed9289d4496246740e59de9'

# create contract
SimpleStoarge = w3.eth.contract(abi=abi, bytecode=bytecode)
