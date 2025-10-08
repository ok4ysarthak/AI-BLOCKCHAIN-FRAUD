import streamlit as st
import pandas as pd
import json
import os
from dotenv import load_dotenv
from web3 import Web3
import numpy as np # <-- 1. IMPORT NUMPY

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Blockchain Fraud Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Environment and Web3 Setup ---
load_dotenv()

RPC_URL = os.getenv("ALCHEMY_API_URL")
if not RPC_URL:
    st.error("RPC URL not found in .env file. Please set ALCHEMY_API_URL or your provider's URL.")
    st.stop()

w3 = Web3(Web3.HTTPProvider(RPC_URL))

# --- Smart Contract Setup ---
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir) 
    abi_path = os.path.join(project_root, "artifacts", "contracts", "RiskRegistry.sol", "RiskRegistry.json")

    with open(abi_path) as f:
        contract_json = json.load(f)
        contract_abi = contract_json["abi"]
except FileNotFoundError:
    st.error(f"Contract ABI file not found. The script looked for it at this path: {abi_path}")
    st.stop()

CONTRACT_ADDRESS = "0x3747c79AcFAC12C11A885Dd248Bc78B6ABe0159D"
try:
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)
except Exception as e:
    st.error(f"Failed to connect to the smart contract. Error: {e}")
    st.stop()

@st.cache_data
def load_risk_data():
    try:
        data_path = os.path.join(project_root, "data", "risk_report.csv")
        df = pd.read_csv(data_path)
        return df
    except FileNotFoundError:
        return None

# --- Sidebar ---
with st.sidebar:
    st.title("🛡️ Fraud Detection Dashboard")
    st.info(
        "This dashboard provides insights from an AI/ML model that analyzes blockchain transactions. "
    )
    
    st.header("Connection Status")
    if not w3.is_connected():
        st.error(f"Failed to connect to the blockchain via your RPC provider.")
    else:
        st.success(f"Connected to Polygon Amoy")
        
    st.header("Contract Details")
    st.write("**Registry Address:**")
    st.code(CONTRACT_ADDRESS, language=None)
    st.link_button("View on PolygonScan", f"https://amoy.polygonscan.com/address/{CONTRACT_ADDRESS}")

    st.markdown("---")
    st.header("How to Use")
    st.write(
        """
        1. **Analyze the Report:** View the table and chart to see addresses flagged by the AI.
        2. **Filter Results:** Use the slider to focus on specific risk score ranges.
        3. **Verify On-Chain:** Copy an address and use the verification tool to get its real-time, tamper-proof score from the blockchain.
        """
    )

# --- Main Page ---
st.title("AI-Powered Blockchain Fraud Detection")
st.markdown("An on-chain risk intelligence platform for the Polygon ecosystem.")

df = load_risk_data()

if df is not None:
    total_flagged = len(df)
    highest_risk = df['risk_score'].max()
    avg_risk = df['risk_score'].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Flagged Addresses", f"{total_flagged}")
    col2.metric("Highest Risk Score", f"{highest_risk}/100")
    col3.metric("Average Risk Score", f"{avg_risk:.2f}/100")
else:
    st.info("Awaiting risk data generation...")

st.markdown("---")

with st.expander("🚀 Project Overview & Use Case"):
    st.markdown(
        """
        **The Problem:** Anonymity on the blockchain, while a core feature, can be exploited for illicit activities like money laundering, scams, and funding terrorism. Identifying these bad actors is crucial for the ecosystem's health and regulatory compliance.

        **Our Solution:** This project demonstrates a powerful system that combines Artificial Intelligence with blockchain technology to create a transparent and reliable risk intelligence tool.
        - **Data-Driven AI:** An offline AI model analyzes transaction patterns to identify suspicious behavior and assign a numerical risk score (0-100) to wallet addresses.
        - **On-Chain Truth:** These risk scores are then permanently recorded on the Polygon blockchain using a smart contract (`RiskRegistry`). This prevents tampering and makes the risk data publicly verifiable by anyone.
        - **Interactive Dashboard:** This Streamlit application serves as the user-friendly interface to view the AI's findings and query the on-chain data in real-time.
        """
    )

with st.expander("💡 Why Store Risk Scores On-Chain?"):
    st.markdown(
        """
        Storing data on a centralized server is efficient, but for risk intelligence, the blockchain provides three indispensable advantages:

        1.  **Immutability:** Once a risk score is recorded on the blockchain, it cannot be altered or deleted. This creates a permanent, tamper-proof audit trail, ensuring data integrity.
        2.  **Transparency:** Anyone in the world can read the data from our `RiskRegistry` smart contract. This allows for public verification and builds trust in the system, as the scores are not hidden in a private database.
        3.  **Decentralization & Availability:** The data is not controlled by a single entity. It is replicated across thousands of nodes in the Polygon network, ensuring it's always available and resistant to censorship or single points of failure.
        """
    )

st.markdown("---")

st.header("Live Risk Analysis")

if df is not None:
    score_range = st.slider(
        'Filter by Risk Score:',
        min_value=0, max_value=100, value=(0, 100)
    )
    
    filtered_df = df[(df['risk_score'] >= score_range[0]) & (df['risk_score'] <= score_range[1])]

    col1, col2 = st.columns([2, 1])

    with col1:
        st.write(f"Displaying {len(filtered_df)} of {len(df)} flagged addresses:")
        st.dataframe(filtered_df, use_container_width=True)
    
    with col2:
        st.write("Score Distribution")
        # --- FIX: Create a proper histogram ---
        # 2. Define the bins (ranges) for the histogram, e.g., 0-10, 10-20, ...
        bins = range(0, 101, 10)
        
        # 3. Use numpy to calculate the number of addresses in each bin
        hist_values, bin_edges = np.histogram(filtered_df['risk_score'], bins=bins)
        
        # 4. Create a new DataFrame for plotting the histogram
        hist_df = pd.DataFrame({
            'Score Range': [f'{bins[i]}-{bins[i+1]}' for i in range(len(bins)-1)],
            'Number of Addresses': hist_values
        }).set_index('Score Range')
        
        # 5. Display the new, corrected bar chart
        st.bar_chart(hist_df)
else:
    st.warning("`data/risk_report.csv` not found. Please generate the report first.")

st.markdown("---")

st.header("On-Chain Risk Score Verification")
st.write("Enter a wallet address to query its current risk score directly from the `RiskRegistry` smart contract.")

address_to_check = st.text_input("Enter Ethereum Address:", placeholder="0x...")

if st.button("Check Risk Score on Blockchain"):
    if not w3.is_address(address_to_check):
        st.error("Invalid Ethereum address. Please check the format.")
    else:
        with st.spinner("Querying the smart contract..."):
            try:
                checksum_address = Web3.to_checksum_address(address_to_check)
                encoded_data = contract.functions.getScore(checksum_address)._encode_transaction_data()
                
                tx_object = {"to": CONTRACT_ADDRESS, "data": encoded_data}
                response = w3.provider.make_request("eth_call", [tx_object, 'latest'])
                
                result_hex = response.get('result')

                if result_hex and result_hex != '0x':
                    score = int(result_hex, 16)
                else:
                    score = 0
                
                st.success(f"**On-Chain Risk Score for `{checksum_address}` is: `{score}`**")
                
                if score > 75:
                    st.warning("🔴 This address has a high risk score. Proceed with extreme caution.")
                elif score > 40:
                    st.info("🟡 This address has a medium risk score.")
                else:
                    st.success("🟢 This address has a low or unset risk score.")

            except Exception as e:
                st.error(f"An error occurred while fetching the score: {e}")

st.markdown("---")
st.write("Developed as a proof-of-concept for AI-driven on-chain intelligence.")

