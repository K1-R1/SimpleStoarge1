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

# connecting to rinkeby
w3 = Web3(Web3.HTTPProvider('https://rinkeby.infura.io/v3/8964f98659f54f2da0768d69459fc06f'))
chain_id = 4
my_address = os.getenv('RINKEBY_ADDRESS')
private_key = os.getenv('RINKEBY_PRIVATE_KEY')

# create contract instance
SimpleStoarge = w3.eth.contract(abi=abi, bytecode=bytecode)
# get latest tx
nonce = w3.eth.getTransactionCount(my_address)

# build tx
tx = SimpleStoarge.constructor().buildTransaction({'chainId': chain_id,'gasPrice': w3.eth.gas_price,'from': my_address,'nonce': nonce})
nonce += 1
#sign tx
signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
# send tx
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print('Contract `SimpleStoarge` successfully deployed')


# interact with deployed contract
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

#Initial value of favouriteNumber
print(f"Initial value of SimpleStoarge's retrive function: {simple_storage.functions.retrieve().call()}")
store_tx = simple_storage.functions.store(894).buildTransaction({'chainId': chain_id,'gasPrice': w3.eth.gas_price,'from': my_address,'nonce': nonce})
signed_store_tx = w3.eth.account.sign_transaction(store_tx, private_key=private_key)
send_signed_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
print('Updating value of favouriteNumber')
store_tx_receipt = w3.eth.wait_for_transaction_receipt(send_signed_store_tx)
#Updated value of favouriteNumber
print(f"Updated value of SimpleStoarge's retrive function: {simple_storage.functions.retrieve().call()}")
