import streamlit as st
import pandas as pd
import numpy as np

import streamlit as st
import pandas as pd

def calculate_bonus(shift_adherence, effective_hours, lam, manual_audits, is_reviewer, full_schedule):
    # Incentive thresholds and bonuses
    bonus_structure = {
        "Shift Adherence": [(14.4, 10), (12.0, 15), (9.6, 25)],
        "Effective Hours": [(90.5, 10), (91.5, 20), (92.5, 40)],
        "LAM": [(81, 15), (83, 30), (85, 50)],
        "Manual Audits": [(95, 15), (96.5, 30), (98, 50)],
    }
    
    # Disqualification condition
    if shift_adherence > 20 and effective_hours < 85:
        return 0
    
    # Calculate individual bonuses
    total_bonus = 0
    for kpi, thresholds in bonus_structure.items():
        user_score = locals()[kpi.lower().replace(" ", "_")]
        for threshold, bonus in reversed(thresholds):
            if user_score >= threshold:
                total_bonus += bonus
                break
    
    # IS Bonus Calculation
    is_bonus = 0
    if is_reviewer == "IS":
        if lam >= 81 and manual_audits >= 95:
            is_bonus = 50
        elif lam >= 81 or manual_audits >= 95:
            is_bonus = 25
        total_bonus += is_bonus
    
    # Full Schedule Bonus
    if full_schedule:
        total_bonus *= 1.15
    
    return round(total_bonus, 2)

# Streamlit UI
st.title("💰 Incentive Bonus Calculator")

# User inputs
shift_adherence = st.number_input("Shift Adherence (minutes)", min_value=0.0, step=0.1)
effective_hours = st.number_input("Effective Hours (%)", min_value=0.0, step=0.1)
lam = st.number_input("LAM (%)", min_value=0.0, step=0.1)
manual_audits = st.number_input("Manual Audits (%)", min_value=0.0, step=0.1)

is_reviewer = st.selectbox("Are you an IS Reviewer?", ["Non-IS", "IS"])
full_schedule = st.checkbox("Did you complete all scheduled hours?")

# Calculate bonus
if st.button("Calculate Bonus"):
    total_bonus = calculate_bonus(shift_adherence, effective_hours, lam, manual_audits, is_reviewer, full_schedule)
    st.success(f"Your total incentive bonus is: €{total_bonus}")
