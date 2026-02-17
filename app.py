import streamlit as st
import extract_msg
import re

def parse_aircraft_sections(text):
    # Splits report into lines to associate flights with specific aircraft 
    lines = text.split('\n')
    aircraft_map = {}
    current_reg = None

    for line in lines:
        # Search for Registration (e.g., G-LCAD) 
        reg_match = re.search(r'G-([A-Z0-9]{4})', line)
        # Search for Flight Numbers (e.g., BA9769T) 
        flight_matches = re.findall(r'BA(\d{1,4}[A-Z]?)', line)

        if reg_match:
            current_reg = reg_match.group(1)[-3:] # Extract last 3 chars 
            if current_reg not in aircraft_map:
                aircraft_map[current_reg] = []
        
        if current_reg and flight_matches:
            for f in flight_matches:
                if f not in aircraft_map[current_reg]:
                    aircraft_map[current_reg].append(f)

    # Build the multi-line output string 
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
        # Process the body text from the msg file 
        raw_result = parse_aircraft_sections(msg.body)
        
        st.success("Allocation String(s) Generated:")
        # Editable text area so you can tweak the result before copying
        final_alloc_text = st.text_area("Edit or Copy Result:", value=raw_result, height=150)
        
    except Exception as e:
        st.error(f"Error: {e}")

st.divider()

# --- SECTION 2: DIVERSION BOX ---
st.header("2. Diversion Input")
# Form allows for 'Enter' key to trigger generation
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

# Logic to display the Diversion string
if submit_button:
    if not flight_num or not stn_1 or not arr_time:
        st.warning("Please fill in the Flight Number, Station, and Arrival Time.")
    else:
        if div_type == "Continue (DIVN)":
            # Format: I DIVN BHX-LCY E1020 WT
            div_final = f"I DIVN {stn_1}-{stn_2} E{arr_time} {reason}"
        else:
            # Format: I DIVT BHX E1020 WT
            div_final = f"I DIVT {stn_1} E{arr_time} {reason}"
        
        st.subheader("Generated Message:")
        st.code(div_final)
