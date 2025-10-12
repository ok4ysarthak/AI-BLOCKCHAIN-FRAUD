
# 🛡️ AI-Powered On-Chain Fraud Detection

<!-- You can add a project banner/header image here -->
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Solidity](https://img.shields.io/badge/Solidity-0.8.24-lightgrey?style=for-the-badge&logo=solidity)](https://soliditylang.org/)
[![Hardhat](https://img.shields.io/badge/Hardhat-Framework-yellow?style=for-the-badge&logo=hardhat)](https://hardhat.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![Polygon](https://img.shields.io/badge/Polygon-Amoy_Testnet-blueviolet?style=for-the-badge&logo=polygon)](https://polygon.technology/)

> A proof-of-concept system that combines a Machine Learning model with a blockchain smart contract to create a transparent and immutable risk intelligence platform for the Web3 ecosystem.

---

## 📖 Table of Contents
* [The Problem](#-the-problem)
* [Our Solution](#-our-solution)
* [What is Blockchain? (A Simple Guide)](#-what-is-blockchain-a-simple-guide)
* [Project Workflow](#-project-workflow)
* [Technology Stack Explained](#-technology-stack-explained)
* [How to Run This Project](#-how-to-run-this-project)
* [The Global Vision: From PoC to Protocol](#-the-global-vision-from-poc-to-protocol)

---

## 😟 The Problem

The world of cryptocurrency offers incredible anonymity and decentralization, but these features are a double-edged sword. They are frequently exploited for illicit activities like money laundering, rug pulls, phishing scams, and hacks, with billions of dollars lost annually. This creates a high-risk environment that erodes user trust, discourages mainstream adoption, and attracts negative regulatory attention.

> **The core question is:** In a decentralized world built on trustless interactions, how can you trust an anonymous digital wallet you're about to interact with?

## ✨ Our Solution

We've built a system that tackles this problem head-on by combining two powerful technologies to create a new layer of on-chain security.

1.  **🧠 Artificial Intelligence (The "Brain"):** An offline AI model analyzes transaction data to identify suspicious wallets. Instead of a simple "good" or "bad" label, it assigns a nuanced **risk score** from 0 to 100, quantifying the level of risk associated with that address.

2.  **⛓️ Blockchain (The "Ledger of Truth"):** These risk scores are then permanently recorded on the Polygon blockchain using a smart contract. This makes the data **immutable (tamper-proof)** and **publicly verifiable** by anyone, at any time.

Essentially, we are creating a decentralized, transparent "risk score" for crypto wallets, moving critical security data from opaque, centralized servers onto an open, auditable public ledger.

**Deployed on Streamlit: https://blockchain-fraud-test.streamlit.app/**

## 🔗 What is Blockchain? (A Simple Guide)

<details>
<summary>Click here to learn the basics of blockchain technology.</summary>

Imagine a shared digital notebook that everyone in a group can see.

* **Shared & Identical:** Every person has an identical copy of this notebook.
* **New Entries:** When someone wants to add a new entry (a "transaction"), they announce it to the group.
* **Group Verification:** The group members check to make sure the entry is valid according to a set of rules.
* **Linked Pages:** Once verified, the new entry is added to a new page (a "block"). This new page is then cryptographically linked to the previous page, creating a **chain of blocks**.
* **Permanent & Unchangeable:** Because all the pages are linked and everyone has a copy, it's virtually impossible for anyone to secretly go back and change an old entry without the entire group noticing and rejecting the change.

This shared, secure, and unchangeable notebook is a **blockchain**. It's a system for storing information that is incredibly difficult to cheat, making it a powerful tool for building trust in a decentralized environment.

</details>

---

## ⚙️ Project Workflow

Our project moves data from raw analysis to a verifiable on-chain record in a few key steps.



1.  **📥 Fetch Data:** We pull raw transaction data from the Polygon Amoy testnet using a Python script (`data_fetcher.py`).
2.  **🤖 AI Analysis:** A machine learning model processes this data, identifies high-risk wallets based on behavioral patterns, and assigns them a risk score. The results are saved to `risk_report.csv`.
3.  **📜 Deploy Contract:** We deploy our `RiskRegistry.sol` smart contract to the Amoy testnet using Hardhat. This contract will act as our permanent, on-chain database for risk scores.
4.  **➡️ Push Scores to Chain:** A script (`push_to_chain.py`) reads the risk report and sends a transaction for each flagged address, calling the `setScore` function on our smart contract to permanently store the score.
5.  **🖥️ Visualize & Verify:** A Streamlit web dashboard (`dashboard.py`) provides a user-friendly interface to view the risk report and allows anyone to enter a wallet address to query its risk score directly from the blockchain in real-time.

---

## 🛠️ Technology Stack Explained

### Blockchain Components
* **Solidity:** The programming language used to write our `RiskRegistry` smart contract. It defines the logic for how risk scores are stored and retrieved on the blockchain.
* **Hardhat:** A professional development environment for Ethereum and EVM-compatible chains. We use it to compile, test, and deploy our Solidity smart contract reliably.
* **Polygon Amoy:** A test version (testnet) of the Polygon network. It allows us to deploy and test our project in a real blockchain environment without spending any real money.
* **Infura/Alchemy:** These are RPC providers. They act as a gateway, giving us a special URL that our Python scripts use to send and receive information from the Polygon blockchain.

### AI & Backend Components
* **Python:** The core programming language for our data analysis, AI model, and blockchain interaction scripts.
* **Pandas & Scikit-learn:** Powerful Python libraries we use to organize the transaction data (Pandas) and build the machine learning model that calculates risk (Scikit-learn).
* **Web3.py:** A crucial Python library that allows our backend scripts to "talk" to the blockchain—to read data and send transactions to our smart contract.

### Frontend
* **Streamlit:** An amazing Python framework that lets us build and launch our interactive web dashboard quickly, allowing for rapid prototyping and visualization.

---

## 🚀 How to Run This Project

### Prerequisites
* [Python](https://www.python.org/downloads/) (version 3.9+)
* [Node.js](https://nodejs.org/en) (version 18+)
* A crypto wallet like [MetaMask](https://metamask.io/) with some testnet Amoy POL from a [faucet](https://faucet.polygon.technology/).

1. Clone the Repository
   ```bash
   git clone <repository-url>
   cd <repository-folder>

2. Setup Python Environment
   ```
   # Create and activate a virtual environment
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate

3. Install Python packages
   ```
   pip install -r requirements.txt
   npm install

4. Configure Environment Variables
   ```
   Create a file named .env in the project root and add the following, replacing the placeholders with your actual credentials

   ###Your RPC URL from Infura or Alchemy
   ALCHEMY_API_URL="[https://polygon-amoy.g.alchemy.com/v2/your-api-key](https://polygon-amoy.g.alchemy.com/v2/your-api-key)"

   # The private key of your wallet (from MetaMask)
   # WARNING: Keep this secret!
   PRIVATE_KEY="0x..."

5. Compile & Deploy Smart Contract
   ```
   npx hardhat compile
   npx hardhat run script/deploy.js --network amoy

   After running, copy the deployed contract address and paste it into the CONTRACT_ADDRESS variables in push_to_chain.py and dashboard.py.

6. Run Backend & AI Scripts
   ```
   python backend/push_to_chain.py
7. Launch the Dashboard
   ```
   streamlit run dashboard.py
   Your browser will open with the interactive dashboard!


## 🔭 The Global Vision: From PoC to Protocol

> This project is a foundational proof-of-concept. To make it a fully functional, global protocol, we would expand it in the following ways:

* **Cross-Chain Interoperability:** Fraud isn't limited to one blockchain. The next step is to make this system work across multiple chains like Ethereum, Solana, and Avalanche. We could use a cross-chain messaging protocol like **Chainlink CCIP** to allow the `RiskRegistry` on Polygon to be queried from any other blockchain, creating a universal risk standard.

* **Decentralized AI & Community Governance:** Currently, our AI model is centralized. The ultimate goal is to move towards a **Decentralized AI (dAI)** model where multiple, independent node operators run the analysis. A **Decentralized Autonomous Organization (DAO)** would govern the model's parameters, preventing any single entity from controlling what is considered "risky" and ensuring the system remains neutral.

* **Incentive Mechanisms & Tokenomics:** A global system needs to be self-sustaining. We could introduce a native utility token to create a crypto-economic model:
    * **Staking:** Users could stake the token to report suspicious addresses, earning rewards if their reports are validated by the AI network.
    * **Rewards:** Node operators who run the AI models and contribute to the network's security would be rewarded with tokens.
    * **Payments:** dApps and other protocols would use the token to pay for API access to the risk data, creating a continuous demand that funds the ecosystem.

* **Public API for Seamless Integration:** We would build a robust, high-availability API. This would allow any developer to easily integrate our risk data into their applications:
    * **Wallets (MetaMask, Phantom):** Could integrate the API to show a warning *before* a user signs a transaction with a high-risk address. 
    * **Decentralized Exchanges (DEXs):** Could use the API to flag or block trades involving addresses with extremely high risk scores, protecting users from scams.
    * **Lending Protocols:** Could automatically adjust collateral requirements based on an address's on-chain risk score.
