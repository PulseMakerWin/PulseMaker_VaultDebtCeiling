# Understanding Oracle Price Feed Mechanisms in Blockchain

## Transaction Analysis: MedianBTCUSD Contract

I analyzed transaction [0xeef51c8f2e5e2a67db2c884ab9cb8e58d8739cb2ad5d0844380945b0701794de](https://scan.mypinata.cloud/ipfs/bafybeih3olry3is4e4lzm7rus5l3h6zrphcal5a7ayfkhzm5oivjro2cp4/#/tx/0xeef51c8f2e5e2a67db2c884ab9cb8e58d8739cb2ad5d0844380945b0701794de?tab=index) to understand the oracle signing mechanism.

The transaction calls the `poke(uint256[],uint256[],uint8[],bytes32[],bytes32[])` function (signature: `0x89bbb8b2`).

## Decoded Transaction Data

### Price Values (BTC/USD)
```
[0]: 87921.0
[1]: 87922.375
[2]: 87922.40000000001
[3]: 87922.40000000001
[4]: 87926.56999999999
[5]: 87934.685
[6]: 87945.265
[7]: 87966.73000000001
[8]: 87974.45
[9]: 88020.05
[10]: 88059.06499999999
[11]: 88096.1
[12]: 88132.5
```

### Timestamps (UTC)
```
[0]: 1731370439 (2024-11-12 00:13:59)
[1]: 1731370407 (2024-11-12 00:13:27)
[2]: 1731370407 (2024-11-12 00:13:27)
[3]: 1731370410 (2024-11-12 00:13:30)
[4]: 1731370441 (2024-11-12 00:14:01)
[5]: 1731370441 (2024-11-12 00:14:01)
[6]: 1731370447 (2024-11-12 00:14:07)
[7]: 1731370403 (2024-11-12 00:13:23)
[8]: 1731370434 (2024-11-12 00:13:54)
[9]: 1731370349 (2024-11-12 00:12:29)
[10]: 1731370396 (2024-11-12 00:13:16)
[11]: 1731370386 (2024-11-12 00:13:06)
[12]: 1731370359 (2024-11-12 00:12:39)
```

### Signature Components
Each price update includes signature components (v, r, s) used to verify the oracle that signed the data.

## Oracle Verification

### Recovered Addresses (Signers)
```
[0]: 0xFbaF3a7eB4Ec2962bd1847687E56aAEE855F5D00
[1]: 0xA8EB82456ed9bAE55841529888cDE9152468635A
[2]: 0x8ff6a38A1CD6a42cAac45F08eB0c802253f68dfD
[3]: 0x8aFBD9c3D794eD8DF903b3468f4c4Ea85be953FB
[4]: 0x16655369Eb59F3e1cAFBCfAC6D3Dd4001328f747
[5]: 0xa580BBCB1Cee2BCec4De2Ea870D20a12A964819e
[6]: 0xd94BBe83b4a68940839cD151478852d16B3eF891
[7]: 0x60da93D9903cb7d3eD450D4F81D402f7C4F71dd9
[8]: 0xDA1d2961Da837891f43235FddF66BAD26f41368b
[9]: 0xaC8519b3495d8A3E3E44c041521cF7aC3f8F63B3
[10]: 0xd72BA9402E9f3Ff01959D6c841DDD13615FFff42
[11]: 0xE6367a7Da2b20ecB94A25Ef06F3b551baB2682e6
[12]: 0xC9508E9E3Ccf319F5333A5B8c825418ABeC688BA
```
### Authorized Oracles
```
[0]: 0x130431b4560Cd1d74A990AE86C337a33171FF3c6
[1]: 0x16655369Eb59F3e1cAFBCfAC6D3Dd4001328f747
[2]: 0x3CB645a8f10Fb7B0721eaBaE958F77a878441Cb9
[3]: 0x4b0E327C08e23dD08cb87Ec994915a5375619aa2
[4]: 0x4f95d9B4D842B2E2B1d1AC3f2Cf548B93Fd77c67
[5]: 0x60da93D9903cb7d3eD450D4F81D402f7C4F71dd9
[6]: 0x71eCFF5261bAA115dcB1D9335c88678324b8A987
[7]: 0x75ef8432566A79C86BBF207A47df3963B8Cf0753
[8]: 0x77EB6CF8d732fe4D92c427fCdd83142DB3B742f7
[9]: 0x83e23C207a67a9f9cB680ce84869B91473403e7d
[10]: 0x8aFBD9c3D794eD8DF903b3468f4c4Ea85be953FB
[11]: 0x8de9c5F1AC1D4d02bbfC25fD178f5DAA4D5B26dC
[12]: 0x8ff6a38A1CD6a42cAac45F08eB0c802253f68dfD
[13]: 0xa580BBCB1Cee2BCec4De2Ea870D20a12A964819e
[14]: 0xA8EB82456ed9bAE55841529888cDE9152468635A
[15]: 0xaC8519b3495d8A3E3E44c041521cF7aC3f8F63B3
[16]: 0xc00584B271F378A0169dd9e5b165c0945B4fE498
[17]: 0xC9508E9E3Ccf319F5333A5B8c825418ABeC688BA
[18]: 0xD09506dAC64aaA718b45346a032F934602e29cca
[19]: 0xD27Fa2361bC2CfB9A591fb289244C538E190684B
[20]: 0xd72BA9402E9f3Ff01959D6c841DDD13615FFff42
[21]: 0xd94BBe83b4a68940839cD151478852d16B3eF891
[22]: 0xDA1d2961Da837891f43235FddF66BAD26f41368b
[23]: 0xE6367a7Da2b20ecB94A25Ef06F3b551baB2682e6
[24]: 0xFbaF3a7eB4Ec2962bd1847687E56aAEE855F5D00
[25]: 0xfeEd00AA3F0845AFE52Df9ECFE372549B74C69D2
```
All recovered addresses match addresses in the authorized oracle list, confirming the legitimacy of the price feeds.

## How Oracle Signatures Work

1. **Signature Creation**:
   - Each oracle signs a message containing: price value, timestamp, and identifier ("BTCUSD")
   - Signatures use ECDSA (Elliptic Curve Digital Signature Algorithm)
   - Components: v (recovery ID), r and s (ECDSA outputs)

2. **Address Recovery**:
   - The contract reconstructs the message hash from the provided data
   - Uses v, r, s to recover the signer's public key
   - Derives the Ethereum address from the public key
   - Verifies the address is in the authorized oracle list

## Oracle System Architecture

### Off-Chain Coordination
1. **Oracle Operations**:
   - Each oracle independently pulls price data from trusted sources
   - Sources likely include major exchanges (Binance, Coinbase, Kraken) and aggregators
   - Oracles sign their price updates off-chain
   - Signed data is sent to a secure API endpoint

2. **Relayer Role**:
   - The relayer (0x48Fc8b... in this case) collects signatures from oracles
   - Validates signatures and checks price ranges
   - Batches multiple signatures into a single transaction
   - Submits the transaction to the blockchain

3. **Benefits**:
   - Gas efficiency (multiple updates in one transaction)
   - Reduced on-chain congestion
   - Centralized coordination with decentralized verification

### Security Considerations
- Communication between oracles and relayer uses secure channels
- System requires protection of private keys
- Infrastructure is typically not open source due to security concerns
- Coordination happens through traditional server infrastructure, not on-chain

## Summary
The transaction shows a sophisticated oracle system where price data is signed off-chain by authorized oracles and submitted in batches by a relayer. The contract verifies each signature to ensure data integrity and authenticity before updating the median price.
