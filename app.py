# --- NEW: CRITICAL FRICTION LOGIC ---

with st.sidebar:
    st.header("🛠️ Tool & Crew Friction")
    heli_standby_days = st.number_input("Heli Standby Days (Grounded by Weather)", value=3)
    standby_fee = st.number_input("Heli Daily Standing Charge ($)", value=4800)
    
    st.header("📂 Data & Audit Risk")
    audit_risk_pct = st.slider("DRFA Claim Rejection Risk (%)", 0, 10, 2, help="Percentage of funding lost due to poor manual evidence.")

# --- UPDATED CALCULATION ENGINE ---

# Aviation Waste: Standby fees + Recon hours that could have been rescue hours
aviation_waste = (heli_standby_days * standby_fee) + (recon_hrs * heli_rate)

# Labor Waste: GIS staff + Field crews hit by 'Information Gaps'
labor_waste = (gis_hours_saved * gis_surge_rate) + (crew_turnbacks * 4 * crew_hr)

# Audit Exposure: The cost of 'bad data' in a multi-million dollar claim
audit_exposure = drfa_claim * (audit_risk_pct / 100)

# TOTAL IMPACT
total_pain_point = (aviation_waste + labor_waste + audit_exposure) * events_per_year
