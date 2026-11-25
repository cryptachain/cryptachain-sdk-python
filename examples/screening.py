"""Address screening examples — single and bulk screening."""

from cryptachain import CryptaChain
from cryptachain.types.screening import RiskLevel

client = CryptaChain(api_key="your-api-key")

# Screen a single address
result = client.screening.screen_address(
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    chain="ethereum",
)
print(f"Address: {result.address}")
print(f"Risk Level: {result.risk_level}")
print(f"Risk Score: {result.risk_score}")
print(f"Sanctions Match: {result.sanctions_match}")

if result.flags:
    print("Flags:")
    for flag in result.flags:
        print(f"  - [{flag.severity}] {flag.flag_type}: {flag.description}")
else:
    print("No flags detected.")

# Bulk screening
print("\n--- Bulk Screening ---\n")
bulk_result = client.screening.screen_bulk([
    {"address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", "chain": "ethereum"},
    {"address": "0xABC0000000000000000000000000000000000001", "chain": "ethereum"},
    {"address": "0xDEF0000000000000000000000000000000000002", "chain": "polygon"},
])

print(f"Screened: {len(bulk_result)}")

for r in bulk_result:
    status = "FLAGGED" if r.sanctions_match else "CLEAN"
    print(f"  {r.address[:10]}... => {status} (risk: {r.risk_level})")

# Check for high-risk addresses
high_risk = [r for r in bulk_result if r.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL)]
if high_risk:
    print(f"\n{len(high_risk)} HIGH/CRITICAL risk addresses found!")

client.close()
