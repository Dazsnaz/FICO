import streamlit as st
import extract_msg
import re

def parse_aircraft_sections(text):
    # This splits the report into sections based on the Aircraft Registration (G-XXXX)
    # It finds all flight numbers associated with that specific registration
    lines = text.split('\n')
    aircraft_map = {}
    current_reg = None

    for line in lines:
        # Look for the Registration (e.g., G-LCAD)
        reg_match = re.search(r'G-([A-Z0-9]{4})', line)
        # Look for Flight Numbers (e.g., BA9769T)
        flight_matches = re.findall(r'BA(\d{1,4}[A-Z]?)', line)

        if reg_match:
            current_reg = reg_match.group(1)[-3:] # Get last 3 (e.g., CAD)
            if current_reg not in aircraft_map:
                aircraft_map[current_reg] = []
        
        if current_reg and flight_matches:
            for f in flight_matches:
                if f not in aircraft_map[current_reg]:
                    aircraft_map[current_reg].append(f)

    # Format each aircraft onto its own new line
    output_lines = []
    for reg, flights in aircraft_map.items():
        if flights:
            output_lines.append(f"I TR T {reg} {' '.join(flights)}")
    
    return "\n".join(output_lines)

st.set_page_config(page_title="Flight Ops Tool", layout="wide")
st.title("✈️ Flight Operations Formatter")

# --- SECTION 1: ALLOCATION CONVERTER ---
st.header("1. Aircraft Allocation")
uploaded_file = st.file_uploader("Drop your .msg report here", type="msg")

if uploaded_file:
    try:
        msg = extract_msg.Message(uploaded_file)
        result = parse_aircraft_sections(msg.body)
        st.success("Allocation String(s) Generated:")
        st.code(result) # This will now show each aircraft on a new line
    except Exception as e:
        st.error(f"Error: {e}")

st.divider()

# --- SECTION 2: DIVERSION BOX ---
st.header("2. Diversion Input")
with st.form("diversion_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        div_type = st.radio("Diversion Type", ["Continue (DIVN)", "Terminate (DIVT)"])
        flight_num = st.text_input("Flight Number", placeholder="e.g., 8465")
    
    with col2:
        if div_type == "Continue (DIVN)":
            stn_1 = st.text_input("Diversion Station", placeholder="BHX")
            stn_2 = st.text_input("Next Station", placeholder="LCY")
        else:
            stn_1 = st.text_input("Terminate Station", placeholder="BHX")
            stn_2 = ""
            
    with col3:
        arr_time = st.text_input("Arrival Time", placeholder="1020")
        reason = st.selectbox("Reason Code", ["WT", "OP", "TD"])

    submit_button = st.form_submit_button("Generate Diversion Message")

if submit_button:
    if not flight_num or not stn_1 or not arr_time:
        st.warning("Please fill in the Flight Number, Station, and Arrival Time.")
    else:
        if div_type == "Continue (DIVN)":
            final_string = f"I DIVN {stn_1}-{stn_2} E{arr_time} {reason}"
        else:
            final_string = f"I DIVT {stn_1} E{arr_time} {reason}"
        
        st.subheader("Generated Message:")
        st.code(final_string) 
