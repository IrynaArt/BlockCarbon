#!/usr/bin/env python3
import argparse
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd

# Average energy consumption per Ethereum transaction in kWh\N{NO-BREAK SPACE}
ENERGY_PER_TX_KWH = 72  
# Average CO2 emitted per kWh of electricity (kg CO2/kWh)
CO2_PER_KWH = 0.475


def get_tx_count(address: str, api_key: str) -> int:
    """
    Get the number of outgoing transactions (nonce) for the given Ethereum address via Etherscan proxy API.
    """
    url = "https://api.etherscan.io/api"
    params = {
        "module": "proxy",
        "action": "eth_getTransactionCount",
        "address": address,
        "tag": "latest",
        "apikey": api_key
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    if "result" not in data:
        raise RuntimeError(f"Etherscan error: {data}")
    return int(data["result"], 16)


def audit_carbon(address: str, api_key: str) -> pd.DataFrame:
    """
    Calculate the carbon footprint for the given Ethereum address.
    Returns a DataFrame with date, address, tx_count, energy_kwh, and co2_kg.
    """
    tx_count = get_tx_count(address, api_key)
    energy = tx_count * ENERGY_PER_TX_KWH
    co2 = energy * CO2_PER_KWH

    record = {
        "date": datetime.utcnow().isoformat(),
        "address": address,
        "transactions": tx_count,
        "energy_kwh": energy,
        "co2_kg": co2
    }
    return pd.DataFrame([record])


def main():
    parser = argparse.ArgumentParser(
        description="Audit the carbon footprint of an Ethereum address."
    )
    parser.add_argument(
        "address", help="Ethereum address to audit"
    )
    parser.add_argument(
        "--api-key", default=None,
        help="Etherscan API key (or set ETHERSCAN_API_KEY in .env)"
    )
    parser.add_argument(
        "--output", default=None,
        help="Path to save CSV report (defaults to stdout)"
    )
    args = parser.parse_args()

    load_dotenv()
    api_key = args.api_key or os.getenv("ETHERSCAN_API_KEY")
    if not api_key:
        parser.error("Etherscan API key is required (use --api-key or set ETHERSCAN_API_KEY)")

    df = audit_carbon(args.address, api_key)
    if args.output:
        df.to_csv(args.output, index=False)
        print(f"Report saved to {args.output}")
    else:
        print(df.to_string(index=False))


if __name__ == "__main__":
    main()
