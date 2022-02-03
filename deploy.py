from solcx import compile_standard, install_solc
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