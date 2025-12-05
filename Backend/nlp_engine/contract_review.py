def analyze_contract_risks(clauses: dict, entities: dict, text: str) -> str:
    """
    Analyzes extracted data to generate a risk report.
    """
    risks = []
    text_lower = text.lower()

    # 1. CLAUSE COMPLETENESS CHECKS
    if not clauses.get("termination"):
        risks.append("🔴 **CRITICAL**: Missing 'Termination' clause. You may be locked into this contract indefinitely.")
    
    if not clauses.get("indemnification"):
        risks.append("🟠 **WARN**: Missing 'Indemnification' clause. High liability risk.")

    if not clauses.get("confidentiality"):
        risks.append("🟡 **NOTE**: No 'Confidentiality' clause found. Ensure trade secrets are protected.")

    # 2. KEYWORD RISK CHECKS (Logic Search)
    if "terminate for convenience" in text_lower:
        risks.append("⚠️ **RISK**: 'Termination for Convenience' detected. The other party can cancel without cause.")
    
    if "auto-renewal" in text_lower or "automatic renewal" in text_lower:
        risks.append("⚠️ **RISK**: 'Auto-Renewal' clause detected. Monitor renewal dates carefully.")

    if "net 60" in text_lower or "net 90" in text_lower:
        risks.append("💰 **PAYMENT**: Long payment terms (Net 60/90) detected.")

    # 3. ENTITY CHECKS
    if not entities.get("effective_dates"):
        risks.append("📅 **DATE**: No effective date found. Contract start time is ambiguous.")

    # 4. FINAL REPORT GENERATION
    if not risks:
        return "✅ **SAFE**: The contract appears to follow standard patterns with no high-level automated risks detected."
    
    return "### Contract Risk Assessment\n" + "\n".join(risks)