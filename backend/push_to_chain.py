# backend/push_to_chain.py
import os, json, time
from dotenv import load_dotenv
from web3 import Web3
import pandas as pd

load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("ALCHEMY_API_URL")))
account = w3.eth.account.from_key(os.getenv("PRIVATE_KEY"))
print("Using address:", account.address)
print("Connected to chain:", w3.is_connected())

with open("artifacts/contracts/RiskRegistry.sol/RiskRegistry.json") as f:
    abi = json.load(f)["abi"]

CONTRACT_ADDRESS = "0x2A9720c20755779362AAd30d278D65e9AA4FD598"
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

def get_nonce_via_rpc(eth_address: str) -> int:
    response = w3.provider.make_request(
        "eth_getTransactionCount",
        [eth_address, 'latest']
    )
    return int(response['result'], 16)

# MODIFICATION 1: The function now accepts the nonce as an argument
def send_score(address: str, score: int, nonce: int):
    print(f"Sending score {score} for {address[:10]}... with nonce {nonce}")
    txn = contract.functions.setScore(address, score).build_transaction({
        "from": account.address,
        "nonce": nonce,
        "gas": 300_000,
        
        # --- THE FINAL FIX ---
        "maxFeePerGas": w3.to_wei("40", "gwei"),      # Total you're willing to pay
        "maxPriorityFeePerGas": w3.to_wei("30", "gwei") # Your tip (must be > 25)
    })
    # ... rest of the function is the same ...
    signed = account.sign_transaction(txn)
    tx_hash = w3.to_hex(w3.keccak(signed.raw_transaction)) # Calculate tx hash before sending
    print(f"Transaction sent with hash: {tx_hash}") # Print hash immediately

    w3.eth.send_raw_transaction(signed.raw_transaction) # Send without assigning return value
    
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"✅ Updated {address[:10]}… → {score} (tx {receipt.transactionHash.hex()[:10]}…)")

def push_all():
    df = pd.read_csv("data/risk_report.csv")
    
    # MODIFICATION 2: Get the starting nonce ONCE before the loop
    start_nonce = get_nonce_via_rpc(account.address)
    print(f"Starting with nonce: {start_nonce}")

    # Use enumerate to get an index `i` for incrementing the nonce
    for i, row in df.head(1).iterrows():
        addr = Web3.to_checksum_address(row["address"])
        score = int(row["risk_score"])
        
        # MODIFICATION 3: Pass the correct, incrementing nonce to the function
        send_score(addr, score, start_nonce + i)
        
        time.sleep(1)

if __name__ == "__main__":
    push_all()