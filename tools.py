"""
tools.py — Risk Assessment Utilities
====================================

This module contains the **risk_score_calculator**, a utility function used by  
the Risk Assessment Agent to convert both objective (FSO-derived) and  
subjective (user-provided) parameters into a structured assessment of the  
client's investment risk profile.

The function evaluates three risk dimensions:

1. **Risk Capacity**  
   Based on long-term financial stability factors such as time horizon,  
   emergency fund depth, and income stability.

2. **Risk Tolerance**  
   Based on the client's behavioral reaction to portfolio volatility.

3. **Risk Exposure / Protection Gaps**  
   Provides qualitative insights such as the need for insurance or risks 
   related to liquidity.

The output is designed to be FSO-friendly and is stored under  
`risk_assessment_data` by the `risk_assessment_agent`.

This tool does NOT modify the FSO directly. It simply returns a structured  
dictionary for the agent to merge into the Financial State Object.
"""

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
    Calculate a user's investment risk score and derive a qualitative risk profile.

    This scoring model combines:
    - **Risk Capacity (Financial Stability)**
    - **Risk Tolerance (Behavioral Response to Volatility)**
    - **Risk Exposure (Protection gaps and liquidity risk)**

    The output is structured for direct insertion into the Financial State Object (FSO)
    under the key `risk_assessment_data`.

    -------------------------------------------------------------------------------
    PARAMETERS
    -------------------------------------------------------------------------------
    time_horizon_years : int
        The user's investment time horizon (in years).  
        - >= 15 years  → More aggressive capacity  
        -   5-14 years → Moderate capacity  
        -   < 5 years  → Conservative capacity  

    emergency_fund_months : int
        Number of months the client can sustain expenses using emergency funds.  
        Thresholds:  
        - >= 6 months → Strong buffer  
        - 3-5 months → Moderate buffer  
        - < 3 months → Weak buffer  

    income_stability_rating : int  
        A subjective score from 1 (unstable) to 5 (highly stable).  
        If the user is *retired with a safe withdrawal rate*, the Risk Agent may assign  
        this value automatically (usually 5).

    volatility_choice : str  
        Behavioral response to a 20% market drop.  
        Accepted patterns (case-insensitive):  
        - "A", "sell" → Conservative  
        - "B", "hold", "hold steady" → Moderate  
        - "C", "invest more" → Aggressive  

    has_dependents : bool  
        Indicates whether the user has financial dependents  
        (used for determining insurance gap severity).

    debt_exceeds_assets : bool  
        Indicates whether the user is in a net-liability position.  
        Used for evaluating liquidity risk.

    -------------------------------------------------------------------------------
    RETURNS
    -------------------------------------------------------------------------------
    Dict[str, Any]:
        {
            "raw_risk_score": int,
                Numerical score (0-100 scale approximation).
            
            "risk_profile": str,
                One of: "Conservative", "Moderate", "Aggressive".
            
            "investment_time_horizon": str,
                Categorized horizon label (e.g., "Long-term (Aggressive Capacity)").
            
            "insurance_gaps": str,
                Guidance on whether additional insurance coverage may be needed.
            
            "liquidity_risk": str,
                High-level assessment of balance sheet risk ("Balanced" or "High Liquidity Risk").
        }

    -------------------------------------------------------------------------------
    NOTES
    -------------------------------------------------------------------------------
    • The scoring logic is intentionally simplified for LLM orchestration workflows.  
    • The agent using this function must ensure correct parsing of qualitative inputs.  
    • The function does NOT handle missing/invalid inputs—validation belongs in the agent.

    -------------------------------------------------------------------------------
    EXAMPLE (OUTPUT)
    -------------------------------------------------------------------------------
    {
        "raw_risk_score": 62,
        "risk_profile": "Aggressive",
        "investment_time_horizon": "Long-term (Aggressive Capacity)",
        "insurance_gaps": "Potential Need for Life and Disability Insurance.",
        "liquidity_risk": "Balanced."
    }
    """

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