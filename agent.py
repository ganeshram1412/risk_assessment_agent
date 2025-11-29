"""
risk_assessment_agent.py
========================

This module defines the **Risk Assessment Agent**, a fully FSO-integrated 
component responsible for determining the user's investment risk profile.

The agent performs a hybrid assessment combining:
- **Objective factors** extracted from the Financial State Object (FSO)
  (e.g., age, retirement status, emergency fund coverage, debt levels).
- **Subjective (qualitative) behavioral traits**, such as market reaction 
  and income stability, collected interactively.

The agent's final responsibility is to call the `risk_score_calculator` tool 
with all required parameters, interpret its output, and update the FSO under 
the key `'risk_assessment_data'`.

This module enables:
- Comprehensive profiling combining tolerance + capacity + risk behavior.
- Tailoring based on life stage (Working vs Retired).
- Clean, single-response updates to the FSO via the ADK-defined Agent interface.

No natural-language explanation should be returned outside the final updated FSO.
"""

from google.adk.agents.llm_agent import Agent
from .tools import risk_score_calculator 
import json 

# --- OPTIMIZED AGENT INSTRUCTION (FSO Integrated) ---
optimized_agent_instruction = """
You are the Financial Risk Analyst. Your goal: establish the user's Risk Profile (tolerance, capacity, protection gaps) by reading data from the Financial State Object (FSO) and asking qualitative questions. Tone: professional and analytical.

**PROCESS MANDATE (FSO-DRIVEN):**

1.  **FSO Input/Output:** You will receive the FSO as a JSON string. Your ONLY output MUST be the **UPDATED FSO**.
2.  **Data Extraction & Initial Notice:**
    * Explain you are using their existing financial data, but need a few quick qualitative answers to finalize their profile.
    * **Crucially, extract the following from FSO:** user_age, user_status, Time Horizon, Emergency Fund Coverage, Debt vs Assets.
3.  **Collect Remaining Qualitative Fields (Interactive):**
    * **Only ask the user the following qualitative questions (as they are not numeric FSO data):**
        * Q3. Income Stability: "Rate your income stability (1=Unstable to 5=Highly stable)." (Note: If Retired, this should default to 5 if drawdown is safe).
        * Q4. Market Reaction: "If your portfolio dropped 20%, would you (A) Sell, (B) Hold, (C) Invest more?"
        * Q5. Dependents: "Do you have financial dependents? (Yes/No)"
4.  **Tool Use:**
    * Compile the 6 required parameters (3 extracted, 3 prompted) into the input structure.
    * Call `risk_score_calculator` with the final parameters.
5.  **FSO Update:**
    * Retrieve the JSON output from the tool (Risk Category, Score, Gaps).
    * Append this analysis to a new key in the FSO, specifically **'risk_assessment_data'**.
6.  **Final Output:** Your *only* response is the fully updated FSO.
"""

# --- AGENT DEFINITION ---
risk_assessment_agent_tool = Agent(
    model='gemini-2.5-flash',
    name='risk_assessment_agent',
    description='Assesses capacity (age/status) and tolerance from the FSO and user input, determines a suitable Investment Profile, identifies Insurance Gaps, and updates the FSO.',
    instruction=optimized_agent_instruction,
    tools=[risk_score_calculator], 
    output_key="financial_state_object"
)