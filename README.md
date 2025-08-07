# BlockCarbon

BlockCarbon is a lightweight Python toolkit to **audit the carbon footprint** of any Ethereum address. By querying the Etherscan API for your transaction count (nonce), it estimates the total energy consumed and CO₂ emitted based on average per-transaction metrics.

## Features

- Fetch outgoing transaction count (nonce) via Etherscan Proxy API
- Estimate total energy consumption (kWh) for the address
- Convert energy consumption to CO₂ emissions (kg)
- Output results as a CSV report or pretty-printed table

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/BlockCarbon.git
   cd BlockCarbon
