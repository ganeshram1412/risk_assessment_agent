# tools.py

from typing import Dict, Any

def risk_score_calculator(
    time_horizon_years: int,
    emergency_fund_months: int,
    income_stability_rating: int,
    volatility_choice: str,
    has_dependents: bool,
    debt_exceeds_assets: bool
) -> Dict[str, Any]:
    """
    Calculates a numerical risk score (0 to 100) based on financial stability 
    and psychological tolerance, and identifies key risk exposures.
    
    A higher score indicates a higher capacity and tolerance for risk.
    """
    score = 0
    max_score = 100
    
    # --- Component 1: Capacity for Risk (Financial Stability) ---
    # Max 40 points

    # Q1: Time Horizon (Tends to be the biggest factor)
    if time_horizon_years >= 15:
        score += 20
        time_category = "Long-term (Aggressive Capacity)"
    elif time_horizon_years >= 5:
        score += 10
        time_category = "Medium-term (Moderate Capacity)"
    else:
        time_category = "Short-term (Conservative Capacity)"

    # Q2: Emergency Fund (High fund = high capacity for risk)
    if emergency_fund_months >= 6:
        score += 10
    elif emergency_fund_months >= 3:
        score += 5
    
    # Q3: Income Stability
    score += (income_stability_rating - 1) * 2.5 # (1 to 5 maps to 0 to 10 points)

    # --- Component 2: Tolerance for Risk (Psychological Comfort) ---
    # Max 30 points
    
    # Q4: Market Volatility
    if volatility_choice.lower() in ('c', 'invest more'):
        score += 30 # Aggressive tolerance
    elif volatility_choice.lower() in ('b', 'hold steady'):
        score += 15 # Moderate tolerance
    # Else: Conservative tolerance (0 points added)

    # --- Component 3: Risk Exposure & Needs ---
    # Does not affect the numerical score, but defines recommendations

    insurance_gap = "Potential Need for Life and Disability Insurance." if has_dependents else "Basic Coverage Only."
    
    liquidity_risk = "High Liquidity Risk and Financial Stress." if debt_exceeds_assets else "Balanced."

    # --- Final Output ---
    
    # Scale score to a percentage (since max_score isn't always 100 with this simple logic)
    # Note: For a real system, you'd make sure the max possible score is 100.
    # For this example, we'll categorize the raw score.
    
    if score >= 60:
        risk_profile = "Aggressive"
    elif score >= 35:
        risk_profile = "Moderate"
    else:
        risk_profile = "Conservative"

    return {
        "raw_risk_score": score,
        "risk_profile": risk_profile,
        "investment_time_horizon": time_category,
        "insurance_gaps": insurance_gap,
        "liquidity_risk": liquidity_risk
    }