# frontend/app.py
import streamlit as st
import pandas as pd
import json
import pathlib
import os
import numpy as np
import plotly.graph_objects as go
from dotenv import load_dotenv
from web3 import Web3

# ------------------- INITIAL SETUP & CONSTANTS -------------------
# Load environment variables
load_dotenv()
ALCHEMY_API_URL = os.getenv("ALCHEMY_API_URL")
CONTRACT_ADDRESS = "0x2A9720c20755779362AAd30d278D65e9AA4FD598"

# Define paths
BASE_DIR = pathlib.Path(__file__).resolve().parents[1]
ABI_PATH = BASE_DIR / "frontend" / "abi" / "RiskRegistry.json"
DATA_PATH = BASE_DIR / "data" / "risk_report.csv"

# ------------------- DATA & WEB3 LOADING (with Caching) -------------------

@st.cache_resource
def get_web3_essentials():
    """Initializes and returns the Web3 instance and contract object."""
    try:
        w3 = Web3(Web3.HTTPProvider(ALCHEMY_API_URL))
        with open(ABI_PATH) as f:
            abi = json.load(f)["abi"]
        contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)
        return w3, contract
    except Exception as e:
        st.error(f"Failed to connect to blockchain. Please check your ALCHEMY_API_URL. Error: {e}")
        return None, None

@st.cache_data
def load_data():
    """Loads the risk report CSV into a pandas DataFrame."""
    df = pd.read_csv(DATA_PATH)
    df["short"] = df["address"].apply(lambda x: f"{x[:6]}…{x[-4:]}")
    # --- Mock data for feature importance visualization ---
    # In a real app, this would come from your AI model's output (e.g., SHAP values)
    np.random.seed(42)
    features = ['Txn Frequency', 'Credential Reuse', 'Anomalous Volume', 'Wallet Age', 'Contract Interaction']
    for idx, row in df.iterrows():
        # Assign random feature importances that roughly add up to the risk score
        importances = np.random.dirichlet(np.ones(5), size=1)[0] * row['risk_score']
        for feature, importance in zip(features, importances):
            df.loc[idx, feature] = importance
    return df

# Initialize web3 and data
w3, contract = get_web3_essentials()
df = load_data()

# ------------------- HELPER FUNCTIONS -------------------

def get_risk_level(score):
    """Determines the risk level and associated color/icon based on a score."""
    if score > 80:
        return "High", "red", "🚨"
    elif score > 50:
        return "Medium", "orange", "⚠️"
    else:
        return "Low", "green", "✅"

def to_checksum(addr: str) -> str:
    """Validates and converts an address to its checksum format."""
    if not Web3.is_address(addr):
        raise ValueError(f"Invalid address: {addr}")
    return Web3.to_checksum_address(addr)

# ------------------- VISUALIZATION FUNCTIONS -------------------

def create_risk_gauge(score, color):
    """Creates a Plotly gauge chart for the given risk score."""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "AI Risk Score", 'font': {'size': 20, 'color': '#FAFAFA'}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "rgba(0,0,0,0.1)",
            'borderwidth': 2,
            'bordercolor': "#333",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(46, 139, 87, 0.3)'},
                {'range': [50, 80], 'color': 'rgba(255, 215, 0, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 80
            }
        },
        number={'font': {'color': '#FAFAFA', 'size': 50}}
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "#FAFAFA", 'family': "Poppins"},
        height=300,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def create_feature_barchart(risk_details, color):
    """Creates a horizontal bar chart for risk feature importance."""
    features = ['Txn Frequency', 'Credential Reuse', 'Anomalous Volume', 'Wallet Age', 'Contract Interaction']
    values = [risk_details[f] for f in features]
    
    fig = go.Figure(go.Bar(
        x=values,
        y=features,
        orientation='h',
        marker_color=color,
        hovertemplate='Risk Contribution: %{x:.2f}<extra></extra>'
    ))
    
    # --- CORRECTED SECTION ---
    fig.update_layout(
        title="Top Contributing Risk Factors",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#FAFAFA",
        margin=dict(l=10, r=10, t=40, b=40),
        xaxis=dict(
            title="Risk Contribution Score",
            gridcolor='#333'
        ),
        # All y-axis properties are now in ONE dictionary
        yaxis=dict(
            title="AI Model Feature",
            autorange="reversed",
            gridcolor='rgba(0,0,0,0)'
        )
    )
    return fig

# ------------------- PAGE CONFIG & STYLES -------------------
st.set_page_config(
    page_title="AI Fraud Detection Dashboard",
    page_icon="🛡️",
    layout="wide",
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
        
        /* CORE THEME */
        body {
            font-family: 'Poppins', sans-serif;
        }
        .main {
            background-color: #0E1117;
            color: #FAFAFA;
        }

        /* CUSTOM CONTAINERS & SECTIONS */
        .block-section {
            background: rgba(22, 27, 34, 0.6);
            border: 1px solid #30363d;
            padding: 30px;
            border-radius: 18px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            margin-top: 25px;
        }
        
        /* METRIC STYLING */
        div[data-testid="stMetric"] {
            background: linear-gradient(145deg, rgba(30, 36, 44, 0.7), rgba(22, 27, 34, 0.7));
            border: 1px solid #30363d;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: all 0.3s ease-in-out;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.4);
        }
        div[data-testid="stMetric"] label {
            font-weight: 600;
            color: #8b949e; /* Lighter gray for label */
        }
        div[data-testid="stMetric"] > div {
            color: #FAFAFA; /* Bright white for value */
        }

        /* SIDEBAR */
        [data-testid="stSidebar"] {
            background-color: #0E1117;
        }

        /* TABS */
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 8px;
            border: 1px solid #30363d;
        }
        .stTabs [aria-selected="true"] {
            background-color: #1c2128;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------- SIDEBAR -------------------
st.sidebar.title("🛡️ Control Panel")
st.sidebar.markdown("Select an address from the dataset or enter one manually.")

# Address selection
address_short = st.sidebar.selectbox(
    "Select a pre-loaded address",
    df["short"],
    index=0,
    help="These are addresses from our risk report dataset."
)
selected_address_raw = df.loc[df["short"] == address_short, "address"].iloc[0]

# Manual input
manual_address = st.sidebar.text_input(
    "Or enter an address manually",
    "",
    placeholder="0x..."
)

# Determine which address to use
if manual_address:
    address_to_analyze_raw = manual_address
else:
    address_to_analyze_raw = selected_address_raw

# ------------------- MAIN DASHBOARD -------------------
st.markdown("<h1 style='text-align:center;'>🛡️ AI-Powered Blockchain Fraud Detector</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#8b949e;'>Fusing on-chain immutability with off-chain AI intelligence.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Main analysis block ---
try:
    # 1. Validate and get address details
    checksum_address = to_checksum(address_to_analyze_raw)
    
    # Check if address is in our CSV, otherwise create a placeholder
    if address_to_analyze_raw in df['address'].values:
        risk_details = df.loc[df['address'] == address_to_analyze_raw].iloc[0]
        risk_score = risk_details["risk_score"]
    else:
        # Placeholder for addresses not in the CSV
        risk_score = 0
        risk_details = pd.Series(
            {'address': address_to_analyze_raw, 'risk_score': 0, 
             'Txn Frequency': 0, 'Credential Reuse': 0, 'Anomalous Volume': 0, 
             'Wallet Age': 0, 'Contract Interaction': 0}
        )
        st.info("This address is not in our pre-analyzed dataset. Displaying on-chain data only.")

    # 2. Fetch On-Chain Score
    with st.spinner(f"Fetching on-chain score for `{checksum_address[:10]}...`"):
        onchain_score = contract.functions.getScore(checksum_address).call()

    # 3. Get dynamic styling based on risk
    risk_level, risk_color, risk_icon = get_risk_level(risk_score)

    # 4. Display Header and Metrics
    st.markdown(f"""
        <div style='text-align: center; margin-bottom: 25px;'>
            <h3 style='margin-bottom: 5px;'>Analysis for Address:</h3>
            <code style='font-size: 1.1rem; background-color: #161B22; padding: 5px 10px; border-radius: 8px;'>{checksum_address}</code>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.plotly_chart(create_risk_gauge(risk_score, risk_color), use_container_width=True)
    
    with col2:
        st.metric(
            label="AI-Derived Risk (Off-Chain)", 
            value=f"{risk_score:.1f}",
            delta=f"{risk_score - onchain_score:.1f} vs On-Chain",
            delta_color="off"
        )
    
    with col3:
        st.metric(
            label="Stored Score (On-Chain)", 
            value=onchain_score
        )

    # 5. Display Detailed Tabs
    st.markdown("<div class='block-section'>", unsafe_allow_html=True)
    tabs = st.tabs(["🧠 AI Insights", "🔗 Blockchain Verification", "ℹ️ About"])

    with tabs[0]:
        st.subheader(f"{risk_icon} AI Risk Assessment: {risk_level}")
        st.write(f"The model has assigned a risk score of **{risk_score:.1f}**, indicating a **{risk_level.lower()}** likelihood of fraudulent activity based on its learned patterns.")
        
        st.plotly_chart(create_feature_barchart(risk_details, risk_color), use_container_width=True)
        
        st.markdown(f"""
            **Key Observations:**
            - **AI/On-Chain Agreement:** The AI score and the on-chain score have a difference of **{abs(risk_score - onchain_score):.1f}** points.
            - **Primary Concern:** `{risk_details[['Txn Frequency', 'Credential Reuse', 'Anomalous Volume']].idxmax()}` was the largest contributor to the risk profile.
        """)

    with tabs[1]:
        st.subheader("Immutable On-Chain Verification")
        st.markdown(f"""
        The score for this address is permanently stored on the Polygon blockchain, ensuring it is tamper-proof and publicly verifiable.
        - **Smart Contract:** `{CONTRACT_ADDRESS}`
        - **Network:** Polygon (or compatible EVM testnet)
        - **Function Called:** `getScore(address)`
        - **Returned Score:** `{onchain_score}`
        
        This on-chain record serves as a decentralized source of truth for the address's risk profile at the time of scoring.
        """)

    with tabs[2]:
        st.subheader("About This Dashboard")
        st.markdown("""
        This system integrates **AI-driven risk assessment** and **blockchain-based verification** to provide a transparent and trustworthy identity fraud detection service.
        
        **Tech Stack:**
        - **🧠 Machine Learning:** Anomaly detection models analyzing transactional behavior.
        - **⛓️ Smart Contract:** A Solidity contract on Polygon for immutable score storage.
        - **🧩 Backend:** Web3.py for blockchain interaction.
        - **🎨 Frontend:** A reactive and beautiful dashboard built with Streamlit.
        """)
        
    st.markdown("</div>", unsafe_allow_html=True)

except ValueError as e:
    st.error(f"⚠️ {e}. Please enter a valid Ethereum address.")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")

# ------------------- FOOTER -------------------
st.markdown("<hr style='border: 1px solid #30363d; margin-top: 50px;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#8b949e;'>© 2025 Blockchain Fraud Detection System | Built with ❤️ and Streamlit</p>", unsafe_allow_html=True)