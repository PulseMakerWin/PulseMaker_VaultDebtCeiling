from web3 import Web3
import time
import pandas as pd
import sys

# Connect to PulseChain
w3 = Web3(Web3.HTTPProvider('https://rpc.pulsechain.com'))

# Contract ABI for Vat contract
vat_abi = [
    {
        "constant": True,
        "inputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "name": "ilks",
        "outputs": [
            {"internalType": "uint256", "name": "Art", "type": "uint256"},
            {"internalType": "uint256", "name": "rate", "type": "uint256"},
            {"internalType": "uint256", "name": "spot", "type": "uint256"},
            {"internalType": "uint256", "name": "line", "type": "uint256"},
            {"internalType": "uint256", "name": "dust", "type": "uint256"}
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {"internalType": "bytes32", "name": "", "type": "bytes32"},
            {"internalType": "address", "name": "", "type": "address"}
        ],
        "name": "urns",
        "outputs": [
            {"internalType": "uint256", "name": "ink", "type": "uint256"},
            {"internalType": "uint256", "name": "art", "type": "uint256"}
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]

def get_collateral_info(vat_contract, ilk_name):
    """Get detailed information about a collateral type."""
    try:
        ilk_identifier = w3.to_bytes(text=ilk_name.ljust(32, '\x00'))
        ilk_data = vat_contract.functions.ilks(ilk_identifier).call()
        
        Art = ilk_data[0] / (10 ** 18)  # wad
        rate = ilk_data[1] / (10 ** 27) # ray
        spot = ilk_data[2] / (10 ** 27) # ray
        line = ilk_data[3] / (10 ** 45) # rad to DAI
        dust = ilk_data[4] / (10 ** 45) # rad to DAI
        
        current_debt = Art * rate
        utilization = (current_debt / line * 100) if line > 0 else 0
        
        return {
            'name': ilk_name,
            'debt_ceiling': line,
            'total_normalized_debt': Art,
            'current_rate': rate,
            'spot_price': spot,
            'dust': dust,
            'current_debt': current_debt,
            'utilization': utilization
        }
    except Exception as e:
        print(f"Error getting collateral info for {ilk_name}: {e}")
        return None

def get_block_timestamp(block_number):
    """Get the timestamp of a block."""
    try:
        block = w3.eth.get_block(block_number)
        timestamp = block['timestamp']
        return time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(timestamp))
    except Exception as e:
        return "Unknown"

def get_vault_info(vat_contract, ilk_name, ilk_info, vault_address):
    """Get detailed information about a vault."""
    try:
        ilk_bytes32 = w3.to_bytes(text=ilk_name.ljust(32, '\x00'))
        urn = vat_contract.functions.urns(ilk_bytes32, vault_address).call()
        
        ink = urn[0] / (10 ** 18)  # collateral amount
        art = urn[1] / (10 ** 18)  # normalized debt
        
        # Calculate current debt and other metrics
        current_debt = art * ilk_info['current_rate']
        collateral_value = ink * ilk_info['spot_price']
        collateralization = (collateral_value / current_debt * 100) if current_debt > 0 else float('inf')
        
        return {
            'collateral_amount': ink,
            'collateral_value_dai': collateral_value,
            'normalized_debt': art,
            'current_debt_dai': current_debt,
            'collateralization_percent': collateralization
        }
    except Exception as e:
        print(f"Error getting vault info: {e}")
        return None

def get_active_vaults(vat_contract, ilk_name, ilk_info):
    """Get active vaults for a collateral type using the CDP Manager."""
    print(f"\nFinding vaults for {ilk_name}...")
    
    try:
        cdp_manager_address = Web3.to_checksum_address("0x5ef30b9986345249bc32d8928B7ee64DE9435E39")
        
        cdp_manager_abi = [
            {
                "constant": True,
                "inputs": [{"name": "", "type": "uint256"}],
                "name": "urns",
                "outputs": [{"name": "", "type": "address"}],
                "payable": False,
                "stateMutability": "view",
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [{"name": "", "type": "uint256"}],
                "name": "ilks",
                "outputs": [{"name": "", "type": "bytes32"}],
                "payable": False,
                "stateMutability": "view",
                "type": "function"
            }
        ]
        
        cdp_manager = w3.eth.contract(address=cdp_manager_address, abi=cdp_manager_abi)
        new_cdp_event = '0x' + w3.keccak(text="NewCdp(address,address,uint256)").hex()

        latest_block = w3.eth.block_number
        start_block = 17237361  #Start block of PulseChain
        block_chunk = 50000  # Process in chunks to show progress
        
        print(f"Scanning blocks {start_block:,} to {latest_block:,}...")
        
        active_vaults = []
        ilk_bytes32 = w3.to_bytes(text=ilk_name.ljust(32, '\x00'))
        
        current_block = start_block
        while current_block < latest_block:
            end_block = min(current_block + block_chunk, latest_block)
            try:
                # Update progress on same line
                sys.stdout.write(f'\rScanning blocks {current_block:,} to {end_block:,} of {latest_block:,} ({((current_block - start_block) / (latest_block - start_block) * 100):.1f}%)')
                sys.stdout.flush()
                
                logs = w3.eth.get_logs({
                    'fromBlock': current_block,
                    'toBlock': end_block,
                    'address': cdp_manager_address,
                    'topics': [new_cdp_event]
                })
                
                for log in logs:
                    try:
                        cdp_id = int(log['topics'][3].hex(), 16)
                        block_number = log['blockNumber']
                        timestamp = get_block_timestamp(block_number)
                        
                        vault_address = cdp_manager.functions.urns(cdp_id).call()
                        vault_ilk = cdp_manager.functions.ilks(cdp_id).call()
                        
                        if vault_ilk == ilk_bytes32:
                            vault_info = get_vault_info(vat_contract, ilk_name, ilk_info, vault_address)
                            
                            if vault_info and (vault_info['collateral_amount'] > 0 or vault_info['normalized_debt'] > 0):
                                vault_data = {
                                    'CDP ID': cdp_id,
                                    'Vault Address': vault_address,
                                    'Creation Date': timestamp,
                                    'Block': block_number,
                                    'Collateral Amount': vault_info['collateral_amount'],
                                    'Collateral Value (DAI)': vault_info['collateral_value_dai'],
                                    'Normalized Debt': vault_info['normalized_debt'],
                                    'Current Debt (DAI)': vault_info['current_debt_dai'],
                                    'Collateralization (%)': vault_info['collateralization_percent']
                                }
                                active_vaults.append(vault_data)
                                print(f"\nFound vault: CDP ID {cdp_id} with debt {vault_data['Current Debt (DAI)']:,.2f} DAI")
                    except Exception as e:
                        continue
                
            except Exception as e:
                print(f"\nError scanning blocks {current_block:,} to {end_block:,}: {str(e)}")
                time.sleep(1)  # Wait before retry
                continue
            
            current_block = end_block + 1
        
        print("\nCompleted vault scan")
        return active_vaults
        
    except Exception as e:
        print(f"Error finding vaults: {e}")
        return []

def main():
    print("MakerDAO Vault Analysis on PulseChain")
    print("=" * 80)
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 80)
    
    # Create contract instance
    vat_address = Web3.to_checksum_address('0x35d1b3f3d7966a1dfe207aa4514c12a259a0492b')
    vat_contract = w3.eth.contract(address=vat_address, abi=vat_abi)
    
    # List of collateral types with non-zero debt from previous scan
    active_collaterals = [
        "ETH-A", "ETH-B", "ETH-C", 
        "WBTC-A", "WBTC-B", "WBTC-C",
        "USDC-A", "USDC-B", 
        "USDT-A", "AAVE-A", "COMP-A", "UNI-A", "YFI-A", "LINK-A", "BAL-A", "CRV-A", "MATIC-A", "WSTETH-A", "RETH-A",
        "BAT-A", "ZRX-A", "KNC-A", "MANA-A", "LRC-A",
        "RENBTC-A", "TUSD-A", "PAXUSD-A", "GUSD-A",
        "PLS-A", "PLSX-A", "HEX-A", "HDRN-A",
        "PSM-USDC-A", "PSM-USDT-A", "PSM-PAX-A", "PSM-GUSD-A",
        "UNIV2DAIETH-A", "UNIV2WBTCETH-A", "UNIV2USDCETH-A",
        "UNIV2DAIUSDC-A", "UNIV2ETHUSDT-A", "UNIV2LINKETH-A",
        "UNIV2UNIETH-A", "UNIV2AAVEETH-A", "UNIV2DAIUSDT-A"
    ]
    
    print(f"\nAnalyzing {len(active_collaterals)} active collateral types...")
    
    # Store results for all collaterals to write later to Excel
    excel_data = {}

    for ilk in active_collaterals:
        info = get_collateral_info(vat_contract, ilk)
        if info:
            print(f"\n{'-'*80}")
            print(f"Collateral Type: {ilk}")
            print(f"Debt Ceiling:         {info['debt_ceiling']:,.2f} DAI")
            print(f"Current Debt:         {info['current_debt']:,.2f} DAI")
            print(f"Utilization:          {info['utilization']:.2f}%")
            print(f"Normalized Debt:      {info['total_normalized_debt']:,.2f}")
            print(f"Current Rate:         {info['current_rate']:.6f}")
            print(f"Spot Price:           {info['spot_price']:.6f}")
            print(f"Minimum Vault Size:   {info['dust']:,.2f} DAI")
            
            # Get vaults for this collateral type
            vaults = get_active_vaults(vat_contract, ilk, info)
            if vaults:
                print(f"\nFound {len(vaults)} active vaults:")
                for vault in sorted(vaults, key=lambda x: x['Current Debt (DAI)'], reverse=True):
                    print(f"\nCDP ID: {vault['CDP ID']}")
                    print(f"Vault Address: {vault['Vault Address']}")
                    print(f"Created: {vault['Creation Date']} (Block {vault['Block']})")
                    print(f"  Collateral Amount:     {vault['Collateral Amount']:,.4f}")
                    print(f"  Collateral Value:      {vault['Collateral Value (DAI)']:,.2f} DAI")
                    print(f"  Normalized Debt:       {vault['Normalized Debt']:,.2f}")
                    print(f"  Current Debt:          {vault['Current Debt (DAI)']:,.2f} DAI")
                    print(f"  Collateralization:     {vault['Collateralization (%)']:,.2f}%")
                    if vault['Current Debt (DAI)'] > 0 and vault['Current Debt (DAI)'] < info['dust']:
                        print("  WARNING: Vault is below dust limit!")
                
                # Store data for Excel
                vaults_df = pd.DataFrame(vaults)
                vaults_df = vaults_df.sort_values(by='Current Debt (DAI)', ascending=False)
                
                summary_data = [
                    ["Collateral Type:", info['name']],
                    ["Debt Ceiling:", f"{info['debt_ceiling']:,.2f} DAI"],
                    ["Current Debt:", f"{info['current_debt']:,.2f} DAI"],
                    ["Utilization:", f"{info['utilization']:.2f}%"],
                    ["Normalized Debt:", f"{info['total_normalized_debt']:,.2f}"],
                    ["Current Rate:", f"{info['current_rate']:.6f}"],
                    ["Spot Price:", f"{info['spot_price']:.6f}"],
                    ["Minimum Vault Size:", f"{info['dust']:,.2f} DAI"]
                ]
                
                excel_data[ilk] = (summary_data, vaults_df)
            else:
                excel_data[ilk] = ([
                    ["Collateral Type:", info['name']],
                    ["Debt Ceiling:", f"{info['debt_ceiling']:,.2f} DAI"],
                    ["Current Debt:", f"{info['current_debt']:,.2f} DAI"],
                    ["Utilization:", f"{info['utilization']:.2f}%"],
                    ["Normalized Debt:", f"{info['total_normalized_debt']:,.2f}"],
                    ["Current Rate:", f"{info['current_rate']:.6f}"],
                    ["Spot Price:", f"{info['spot_price']:.6f}"],
                    ["Minimum Vault Size:", f"{info['dust']:,.2f} DAI"]
                ], pd.DataFrame())  # Empty DataFrame if no vaults found
    
    print("\nWriting results to Excel file...")
    
    # Write results to an Excel file, each collateral on a separate sheet
    with pd.ExcelWriter("MakerDAO_Vaults.xlsx", engine="xlsxwriter") as writer:
        for ilk, (summary_data, vaults_df) in excel_data.items():
            # Write summary data at the top
            worksheet = writer.book.add_worksheet(ilk.replace("/", "_"))
            # Write the summary info
            for i, row in enumerate(summary_data):
                worksheet.write(i, 0, row[0])
                worksheet.write(i, 1, row[1])
            
            # Leave a blank line after summary
            start_row = len(summary_data) + 2
            
            if not vaults_df.empty:
                # Write vaults DataFrame below
                vaults_df.to_excel(writer, sheet_name=ilk.replace("/", "_"), startrow=start_row, index=False)
            
    print("\nData successfully written to MakerDAO_Vaults.xlsx")

if __name__ == "__main__":
    main()
