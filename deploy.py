from os import getenv

from web3 import Web3

from compile_functions import compile_with_output_file, get_abi_and_bytecode


def deploy():
    compiled_sol = compile_with_output_file("SimpleStorage", "0.6.0")
    abi, bytecode = get_abi_and_bytecode(compiled_sol)

    # Connection info
    w3 = Web3(Web3.HTTPProvider(getenv("HTTP_PROVIDER")))
    chain_id = getenv("CHAIN_ID")
    my_address = getenv("MY_ADDRESS")
    private_key = getenv("PRIVATE_KEY")

    # Create contract
    SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
    # Get nonce from latest transaction count
    nonce = w3.eth.getTransactionCount(my_address)
    # Build -> Sign -> Send transaction
    transaction = SimpleStorage.constructor().buildTransaction(
        {"chainId": chain_id, "from": my_address, "nonce": nonce}
    )
    signed_transaction = w3.eth.account.sign_transaction(
        transaction, private_key=private_key
    )

    print("Depoying Contract...")
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
    print("Deployed!")

    # Working with the contract -> Contract Address / Contract ABI
    simple_storage = w3.eth.contract(
        address=transaction_receipt.contractAddress, abi=abi
    )

    # Interaction -> Call / Transaction

    print(f"Value of favouriteNumber: {simple_storage.functions.retrieve().call()}")
    print("Contract Transaction Initiating...")
    store_transaction = simple_storage.functions.store(15).buildTransaction(
        {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
    )
    signed_store_transaction = w3.eth.account.sign_transaction(
        store_transaction, private_key=private_key
    )
    store_transaction_hash = w3.eth.send_raw_transaction(
        signed_store_transaction.rawTransaction
    )
    store_transaction_receipt = w3.eth.wait_for_transaction_receipt(
        store_transaction_hash
    )
    print("Contract Transaction Complete!")

    print(f"Value of favouriteNumber: {simple_storage.functions.retrieve().call()}")
