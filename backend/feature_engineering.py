# backend/feature_engineering.py
import pandas as pd
import numpy as np

RAW_CSV = "data/raw_transactions.csv"
OUT_CSV = "data/identity_features.csv"

def build_features():
    df = pd.read_csv(RAW_CSV)
    # Convert timestamp to datetime
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')

    # 1️⃣ Total number of tx per address
    tx_counts = df.groupby('from').size().rename('tx_count')

    # 2️⃣ Average daily tx rate
    days = (df['datetime'].max() - df['datetime'].min()).days + 1
    tx_rate = (tx_counts / days).rename('tx_per_day')

    # 3️⃣ Total ETH/MATIC transferred out (in wei) – watch for 0‑value txs
    out_value = df.groupby('from')['value_wei'].sum().rename('total_out_wei')

    # 4️⃣ Distinct counterparties (unique receivers)
    uniq_to = df.groupby('from')['to'].nunique().rename('unique_receivers')

    # 5️⃣ Gas price statistics
    gas_stats = df.groupby('from')['gas_price_wei'].agg(['mean','std','max']).rename(
        columns={'mean':'gas_price_mean','std':'gas_price_std','max':'gas_price_max'})

    # 6️⃣ Time‑gap features (seconds between consecutive txs)
    df = df.sort_values(['from','datetime'])
    df['prev_ts'] = df.groupby('from')['timestamp'].shift(1)
    df['gap_seconds'] = df['timestamp'] - df['prev_ts']
    gap_stats = df.groupby('from')['gap_seconds'].agg(['mean','std','min','max']).fillna(0)
    gap_stats = gap_stats.rename(columns=lambda c: f'gap_{c}')

    # Merge everything
    features = pd.concat([tx_counts, tx_rate, out_value, uniq_to, gas_stats, gap_stats], axis=1).reset_index()
    features.to_csv(OUT_CSV, index=False)
    print(f"Feature table saved to {OUT_CSV}")
    return features

if __name__ == "__main__":
    build_features()
