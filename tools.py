# tools.py

from google.adk.agents.llm_agent import AgentTool
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

# --- Register the Tool for ADK ---

calculate_risk_score = AgentTool(
    name="calculate_risk_score",
    description="Calculates a comprehensive numerical risk score and profile based on the user's financial capacity, tolerance, and exposure to risk.",
    func=risk_score_calculator,
    schema={
        "type": "object",
        "properties": {
            "time_horizon_years": {"type": "integer", "description": "The longest investment time frame in years."},
            "emergency_fund_months": {"type": "integer", "description": "Number of months of expenses covered by the emergency fund."},
            "income_stability_rating": {"type": "integer", "description": "Income stability rating from 1 (Unstable) to 5 (Stable)."},
            "volatility_choice": {"type": "string", "description": "User's response to the 20% drop question (A, B, or C)."},
            "has_dependents": {"type": "boolean", "description": "True if the user has financial dependents."},
            "debt_exceeds_assets": {"type": "boolean", "description": "True if non-mortgage debt is greater than liquid assets."}
        },
        "required": ["time_horizon_years", "emergency_fund_months", "income_stability_rating", "volatility_choice", "has_dependents", "debt_exceeds_assets"]
    }
)