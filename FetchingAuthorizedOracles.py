import json
from web3 import Web3

# Connect to an Ethereum node
w3 = Web3(Web3.HTTPProvider('https://rpc.pulsechain.com'))

# Contract address
contract_address = '0xe0F30cb149fAADC7247E953746Be9BbBB6B5751f'

# ABI as a JSON string
abi_json = '''
[
    {
        "anonymous": false,
        "inputs": [
            {"indexed": false, "internalType": "uint256", "name": "val", "type": "uint256"},
            {"indexed": false, "internalType": "uint256", "name": "age", "type": "uint256"}
        ],
        "name": "LogMedianPrice",
        "type": "event"
    },
    {
        "anonymous": true,
        "inputs": [
            {"indexed": true, "internalType": "bytes4", "name": "sig", "type": "bytes4"},
            {"indexed": true, "internalType": "address", "name": "usr", "type": "address"},
            {"indexed": true, "internalType": "bytes32", "name": "arg1", "type": "bytes32"},
            {"indexed": true, "internalType": "bytes32", "name": "arg2", "type": "bytes32"},
            {"indexed": false, "internalType": "bytes", "name": "data", "type": "bytes"}
        ],
        "name": "LogNote",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "age",
        "outputs": [{"internalType": "uint32", "name": "", "type": "uint32"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "bar",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "bud",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "usr", "type": "address"}],
        "name": "deny",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address[]", "name": "a", "type": "address[]"}],
        "name": "diss",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "a", "type": "address"}],
        "name": "diss",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address[]", "name": "a", "type": "address[]"}],
        "name": "drop",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address[]", "name": "a", "type": "address[]"}],
        "name": "kiss",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "a", "type": "address"}],
        "name": "kiss",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address[]", "name": "a", "type": "address[]"}],
        "name": "lift",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "orcl",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "peek",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"},
            {"internalType": "bool", "name": "", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256[]", "name": "val_", "type": "uint256[]"},
            {"internalType": "uint256[]", "name": "age_", "type": "uint256[]"},
            {"internalType": "uint8[]", "name": "v", "type": "uint8[]"},
            {"internalType": "bytes32[]", "name": "r", "type": "bytes32[]"},
            {"internalType": "bytes32[]", "name": "s", "type": "bytes32[]"}
        ],
        "name": "poke",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "read",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "usr", "type": "address"}],
        "name": "rely",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "bar_", "type": "uint256"}],
        "name": "setBar",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "name": "slot",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "wards",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "wat",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "view",
        "type": "function"
    }
]
'''

# Load the ABI
abi = json.loads(abi_json)

# Create contract instance
contract = w3.eth.contract(address=contract_address, abi=abi)

# Fetch oracles from 'slot' mapping
oracles = []
for i in range(256):
    address = contract.functions.slot(i).call()
    if address != '0x0000000000000000000000000000000000000000':
        oracles.append(address)

print("\nAuthorized Oracles:")
print("===================")
for idx, oracle_address in enumerate(oracles):
    print(f"  [{idx}]: {oracle_address}")
