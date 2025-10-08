import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()
w3 = Web3(Web3.HTTPProvider(os.getenv("ALCHEMY_API_URL")))
print("Connected:", w3.is_connected())
