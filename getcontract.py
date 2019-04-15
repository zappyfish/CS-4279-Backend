import json
import web3

from web3 import Web3
from solc import compile_source
from web3.contract import ConciseContract


w3 = Web3(Web3.EthereumTesterProvider())

w3.eth.defaultAccount = w3.eth.accounts[0]

abi = [{'constant': False, 'inputs': [{'name': '_greeting', 'type': 'string'}], 'name': 'setGreeting', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'greet', 'outputs': [{'name': '', 'type': 'string'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'greeting', 'outputs': [{'name': '', 'type': 'string'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'constructor'}]

contract_address="0xF2E246BB76DF876Cef8b38ae84130F4F55De395b"

user = w3.eth.contract(address=contract_address, abi=abi)

print(user.functions.greet().call())
