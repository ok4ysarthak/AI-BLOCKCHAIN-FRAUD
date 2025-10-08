import pandas as pd
from tqdm import tqdm
from web3 import Web3
from dotenv import load_dotenv
import os
import time

load_dotenv()
w3 = Web3(Web3.HTTPProvider(os.getenv("ALCHEMY_API_URL")))

print("Connected:", w3.is_connected())

def get_raw_block_data(block_number: int):
    """
    Makes a direct RPC call to get the block data as a raw dictionary,
    bypassing web3.py's PoA validation.
    """

    response = w3.provider.make_request(
        "eth_getBlockByNumber", 
        [hex(block_number), True]
    )
    
    if 'result' in response:
        return response['result']
    else:
        raise ConnectionError(f"RPC call failed for block {block_number}: {response.get('error')}")

def collect_address_stats(start_block: int, end_block: int, csv_path: str = "data/raw_transactions.csv"):
    rows = []
    for bn in tqdm(range(start_block, end_block + 1)):
        try:
            # 1. Use our new function to get raw block data
            block_dict = get_raw_block_data(bn)
            
            # The node can sometimes return null for a block that doesn't exist yet
            if block_dict is None:
                print(f"Block {bn} returned null, skipping.")
                continue

            # 2. Access data using dictionary keys, not attributes
            txns = block_dict.get('transactions', [])
            
            # 3. Manually convert hex values to integers
            block_timestamp = int(block_dict['timestamp'], 16)

        except Exception as e:
            print(f"Block {bn} failed: {e}")
            continue

        for tx in txns:
            rows.append({
                "block": bn,
                "tx_hash": tx['hash'], # Already a hex string
                "from": tx['from'],
                "to": tx['to'],
                "value_wei": int(tx['value'], 16), # Convert hex to int
                "gas_price_wei": int(tx['gasPrice'], 16), # Convert hex to int
                "timestamp": block_timestamp
            })
        time.sleep(0.05)

    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df.to_csv(csv_path, index=False)
    print(f"Saved {len(df)} rows to {csv_path}")


if __name__ == "__main__":
    # Use a recent block range from Polygon Amoy
    latest = 6125500 
    start = latest - 200      
    end   = latest          
    collect_address_stats(start, end)