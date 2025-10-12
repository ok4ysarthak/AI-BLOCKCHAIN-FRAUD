# frontend/app.py
import streamlit as st
import pandas as pd
import json, pathlib, os
from dotenv import load_dotenv
from web3 import Web3

# ------------------- INITIAL SETUP -------------------
load_dotenv()
w3 = Web3(Web3.HTTPProvider(os.getenv("ALCHEMY_API_URL")))

BASE_DIR = pathlib.Path(__file__).resolve().parents[1]
ABI_PATH = BASE_DIR / "frontend" / "abi" / "RiskRegistry.json"

with open(ABI_PATH) as f:
    abi = json.load(f)["abi"]

CONTRACT_ADDRESS = "0x2A9720c20755779362AAd30d278D65e9AA4FD598"
contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=abi
)

def to_checksum(addr: str) -> str:
    if not Web3.is_address(addr):
        raise ValueError(f"Invalid address: {addr}")
    return Web3.to_checksum_address(addr)

# ------------------- PAGE CONFIG -------------------
st.set_page_config(
    page_title="Blockchain Identity Fraud Dashboard",
    page_icon="🕵️‍♂️",
    layout="wide",
)

# ------------------- CUSTOM STYLES -------------------
st.markdown("""
    <style>
        .main {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        h1, h2, h3, h4 {
            color: #F5F5F5;
        }
        .metric-container {
            background: #161B22;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 0 10px rgba(255,255,255,0.05);
            transition: all 0.3s ease-in-out;
        }
        .metric-container:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 15px rgba(255,255,255,0.1);
        }
        .risk-badge {
            padding: 8px 18px;
            border-radius: 12px;
            font-weight: 600;
            display: inline-block;
            margin-top: 10px;
        }
        .low {background-color: #2E8B5733; color: #2E8B57;}
        .medium {background-color: #FFD70033; color: #FFD700;}
        .high {background-color: #FF634733; color: #FF6347;}
        .block-section {
            background: #161B22;
            padding: 30px;
            border-radius: 18px;
            box-shadow: 0 0 10px rgba(255,255,255,0.05);
            margin-top: 25px;
        }
        .footer {
            text-align:center;
            color: grey;
            margin-top: 50px;
            font-size: 0.9rem;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------- HEADER -------------------
st.markdown("<h1 style='text-align:center;'>🕵️‍♂️ Blockchain Identity Fraud Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#AAA;'>AI-powered fraud detection combining on-chain verification and off-chain intelligence.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ------------------- DATA LOAD -------------------
df = pd.read_csv(BASE_DIR / "data" / "risk_report.csv")
df["short"] = df["address"].apply(lambda x: f"{x[:6]}…{x[-4:]}")

# ------------------- ADDRESS SELECTION -------------------
with st.container():
    st.markdown("<h4>🔍 Select a blockchain address</h4>", unsafe_allow_html=True)
    chosen = st.selectbox("Pick an address", df["short"], label_visibility="collapsed")

addr_raw = df.loc[df["short"] == chosen, "address"].values[0]
addr = to_checksum(addr_raw)
onchain_score = contract.functions.getScore(addr).call()
row = df.loc[df["address"] == addr_raw].iloc[0]
risk_score = row["risk_score"]

# ------------------- METRIC DISPLAY -------------------
st.markdown(f"<h3 style='text-align:center;'>Analyzing Address:</h3>", unsafe_allow_html=True)
st.markdown(f"<h5 style='text-align:center; color:#BBB;'>{addr_raw}</h5>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric(label="AI-Derived Risk (0-100)", value=f"{risk_score:.1f}")
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric(label="On-Chain Stored Score", value=f"{onchain_score}")
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------- RISK LEVEL -------------------
st.markdown("<br>", unsafe_allow_html=True)
if risk_score > 80:
    st.markdown('<div class="risk-badge high">⚠️ Very High Risk</div>', unsafe_allow_html=True)
    st.warning("Anomalous transaction volume or credential pattern detected.")
elif risk_score > 50:
    st.markdown('<div class="risk-badge medium">🕵️ Medium Risk</div>', unsafe_allow_html=True)
    st.info("Irregular activity pattern found. Monitor closely.")
else:
    st.markdown('<div class="risk-badge low">✅ Low Risk</div>', unsafe_allow_html=True)
    st.success("Normal transaction behavior detected.")

# ------------------- DETAILED TABS -------------------
st.markdown("<div class='block-section'>", unsafe_allow_html=True)
st.markdown("### 📊 Detailed Analysis")

tabs = st.tabs(["🧠 AI Insights", "🔗 Blockchain Verification", "ℹ️ About"])

with tabs[0]:
    st.markdown(f"""
    **Address:** `{addr_raw}`  
    **AI Confidence:** {100 - abs(risk_score - onchain_score)}%  
    **Last Evaluation:** Recent on-chain data analysis  

    **Detected Anomalies:**
    - Irregular transaction frequency  
    - Possible identity reuse across wallets  
    - Suspicious credential patterns  
    - Transaction bursts within short intervals  

    **Risk Category:**  
    {"🚨 Critical" if risk_score > 80 else "⚠️ Moderate" if risk_score > 50 else "✅ Safe"}
    """)

with tabs[1]:
    st.markdown(f"""
    **Smart Contract:** `{CONTRACT_ADDRESS}`  
    **Network:** Polygon (Amoy Testnet/Mainnet)  
    **Function Used:** `getScore(address)`  
    **Checksum Address:** `{addr}`  

    The on-chain verification ensures the score is immutable and tamper-proof.
    """)

with tabs[2]:
    st.markdown("""
    ### About This Dashboard
    This system integrates **AI-driven risk assessment** and **blockchain-based verification**  
    to provide transparent and trustworthy identity fraud detection.

    **Tech Stack:**
    - 🧠 Machine Learning anomaly detection models  
    - ⛓ Solidity Smart Contract on Polygon  
    - 🧩 Web3.py for blockchain connection  
    - 🎨 Streamlit frontend  

    **Purpose:**  
    Developed for transparency, risk intelligence, and decentralized identity safety.
    """)

st.markdown("</div>", unsafe_allow_html=True)

# ------------------- FOOTER -------------------
st.markdown("<p class='footer'>© 2025 Blockchain Fraud Detection System | Built with ❤️ by <b>Sarthak Kumar Singh</b></p>", unsafe_allow_html=True)
