# frontend/app.py
import streamlit as st
import pandas as pd
import json, pathlib, os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()
w3 = Web3(Web3.HTTPProvider(os.getenv("ALCHEMY_API_URL")))

BASE_DIR = pathlib.Path(__file__).resolve().parents[1]   # project root
ABI_PATH = BASE_DIR / "artifacts" / "contracts" / "RiskRegistry.sol" / "RiskRegistry.json"
with open(ABI_PATH) as f:
    abi = json.load(f)["abi"]

CONTRACT_ADDRESS = "0xYOUR_AMOY_DEPLOYED_RISKREGISTRY_ADDRESS"
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

st.title("🕵️‍♂️ Blockchain Identity Fraud Dashboard")

df = pd.read_csv(BASE_DIR / "data" / "risk_report.csv")
df["short"] = df["address"].apply(lambda x: f"{x[:6]}…{x[-4:]}")
chosen = st.selectbox("Pick an address", df["short"])

addr = df.loc[df["short"] == chosen, "address"].values[0]
onchain_score = contract.functions.getScore(addr).call()
row = df.loc[df["address"] == addr].iloc[0]

st.subheader(f"Address {addr}")
st.metric("AI‑derived risk (0‑100)", f"{row['risk_score']:.1f}")
st.metric("On‑chain stored score", f"{onchain_score}")

if row["risk_score"] > 80:
    st.warning("⚠️ Very high risk – anomalous transaction volume or credential pattern.")
elif row["risk_score"] > 50:
    st.info("🔎 Medium risk – watch the activity.")
else:
    st.success("✅ Low risk – looks normal.")
