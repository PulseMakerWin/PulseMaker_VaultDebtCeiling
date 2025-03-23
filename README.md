# MakerDAO Vault Analysis for PulseChain

This tool analyzes MakerDAO vaults on PulseChain, providing detailed information about collateral types, debt ceilings, and individual vaults.

## Features

- Retrieves debt ceiling and utilization for all active collateral types
- Identifies and analyzes active vaults for each collateral type
- Calculates key metrics like collateralization ratio and debt amounts
- Exports all data to a well-formatted Excel file

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/makerdao-vault-analysis.git
   cd makerdao-vault-analysis
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage


Run the script with:

```
python VaultsDebtCeiling.py
```

The script will:
1. Connect to PulseChain RPC
2. Analyze all active collateral types
3. Find and analyze all vaults for each collateral type
4. Output results to the console and to `MakerDAO_Vaults.xlsx`

## Output

The script generates an Excel file with:
- One sheet per collateral type
- Summary information at the top of each sheet
- Detailed information about each vault
- Sorted by debt amount (largest first)

## Requirements

- Python 3.7+
- Web3.py
- Pandas
- XlsxWriter

## License

MIT 