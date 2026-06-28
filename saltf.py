from web3 import Web3
from eth_utils import keccak, to_bytes
import secrets
import time

FACTORY_ADDRESS = Web3.to_checksum_address("0x699d4368C14cEB7F85582Ef6c0a4E981E80bdE6F")
DEPLOYER_ADDRESS = Web3.to_checksum_address("0x456eB09D70E0A394E945488A64F92FaCCdCdD00C")
DESIRED_SUFFIX = "0xf15c7f1f76388520b70505e9cc285a8b18d9a21f"

BYTECODE = "0x608060405234801562000010575f80fd5b50336040518060400160405280601881526020017f546574686572205553442042726964676564205a454432300000000000000000815250604051806040016040528060068152602001652aa9a22a173d60d11b81525081600390816200007891906200038e565b5060046200008782826200038e565b5050506001600160a01b038116620000b957604051631e4fbdf760e01b81525f60048201526024015b60405180910390fd5b620000c48162000132565b50620000ee33620000d86012600a62000565565b620000e8906311e1a3006200057c565b62000183565b604051734be35ec329343d7d9f548d42b0f8c17fffe07db4907f8e1a1422bcae26470358ddb7b260bfc26f09df419f35e3d1e2da1b82506308b9905f90a2620005ac565b..."

bytecode_bytes = bytes.fromhex(BYTECODE[2:])
bytecode_hash = keccak(bytecode_bytes)

def compute_create2_address(salt_bytes):
    packed = (
        b'\xff' +
        bytes.fromhex(FACTORY_ADDRESS[2:]) +
        salt_bytes +
        bytecode_hash
    )

    address_bytes = keccak(packed)[12:]
    return "0x" + address_bytes.hex()

print("START SEARCH suffix:", DESIRED_SUFFIX)
print("Bytecode hash:", "0x" + bytecode_hash.hex())
print()

attempts = 0
start_time = time.time()

desired = DESIRED_SUFFIX.lower().replace("0x","")

while True:
    salt_bytes = secrets.token_bytes(32)
    address = compute_create2_address(salt_bytes)

    attempts += 1

    if attempts % 10000 == 0:
        elapsed = time.time() - start_time
        rate = int(attempts / elapsed)
        print(f"TRY: {attempts:,} | SPEED: {rate:,}/s | LAST ADDRESS: {address}")

    if address.lower().endswith(desired):
        print("\n✅ FOUND!")
        print("Salt:", "0x" + salt_bytes.hex())
        print("LAST ADDRESS:", address)
        print("TRY ATTEMPT:", f"{attempts:,}")
        print("TIME:", int(time.time() - start_time), "SECONDS")
        break
