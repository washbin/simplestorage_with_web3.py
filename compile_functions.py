from json import dump
from os import makedirs, path

from solcx import compile_standard, install_solc


def compile_with_output_file(smart_contract_file: str, compiler_version: str):
    with open(f"./contracts/{smart_contract_file}.sol", "r") as file:
        simple_storage_file = file.read()

    # Installing compiler
    install_solc(compiler_version)
    # Compiling
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version=compiler_version,
    )

    if not path.exists("output"):
        makedirs("output")
    with open(f"./output/{smart_contract_file}.json", "w") as file:
        dump(compiled_sol, file)

    return compiled_sol


def get_abi_and_bytecode(compiled_sol):

    # ABI
    abi = (
        compiled_sol["contracts"]
        .get("SimpleStorage.sol")
        .get("SimpleStorage")
        .get("abi")
    )

    # Bytecode
    bytecode = (
        compiled_sol["contracts"]
        .get("SimpleStorage.sol")
        .get("SimpleStorage")
        .get("evm")
        .get("bytecode")
        .get("object")
    )

    return abi, bytecode
