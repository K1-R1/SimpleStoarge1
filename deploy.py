from solcx import compile_standard, install_solc
from web3 import Web3

import json, os

from dotenv import load_dotenv
load_dotenv()

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
my_address = os.getenv('ADDRESS')
private_key = os.getenv('PRIVATE_KEY')

# create contract instance
SimpleStoarge = w3.eth.contract(abi=abi, bytecode=bytecode)

# get latest tx
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)

# build tx
tx = SimpleStoarge.constructor().buildTransaction({'chainId': chain_id,'from': my_address,'nonce': nonce})

#sign tx