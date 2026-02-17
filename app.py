import streamlit as st
import extract_msg
import re

def parse_aircraft_data(text):
    # 1. Extract Registration Suffix (e.g., G-LCAD -> CAD)
    # This looks for G- followed by 4 letters, then takes the last 3
    reg_match = re.search(r'G-([A-Z0-9]{4})', text)
    if reg_match:
        full_reg = reg_match.group(1)
        aircraft_suffix = full_reg[-3:] # Takes 'CAD' from 'LCAD'
    else:
        aircraft_suffix = "CAD"
    
    # 2. Extract Flight Numbers
    # Looks for 'BA' followed by 1-4 digits and an optional letter (T)
    # Example: BA9769T, BA4466
    flights = re.findall(r'BA(\d{1,4}[A-Z]?)', text)
    
    # Remove duplicates while keeping the original order
    unique_flights = []
    for f in flights:
        if f not in unique_flights:
            unique_flights.append(f)
    
    # 3. Final Format
    return f"I TR T {aircraft_suffix} {' '.join(unique_flights)}"

st.set_page_config(page_title="Flight Ops Tool", layout="wide")
st.title("✈️ Flight Operations Formatter")

# --- SECTION 1: ALLOCATION CONVERTER ---
st.header("1. Aircraft Allocation")
uploaded_file = st.file_uploader("Drop your .msg report here", type="msg")

if uploaded_file:
    try:
        msg = extract_msg.Message(uploaded_file)
        # Use both body and subject just in case the data is split
        combined_text = f"{msg.subject} {msg.body}"
        result = parse_aircraft_data(combined_text)
        st.success("Allocation String Generated:")
        st.code(result)
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
        st.code(final_string)import streamlit as st
import extract_msg
import re

def parse_aircraft_data(text):
    # [cite_start]Extracts the last 3 letters of the registration [cite: 1]
    reg_match = re.search(r'G-LC([A-Z]{2})', text)
    aircraft_suffix = reg_match.group(1) if reg_match else "CAD"
    
    # [cite_start]Extracts flight numbers by removing 'BA' prefix [cite: 1]
    flights = re.findall(r'BA(\d{1,4}[A-Z]?)', text)
    
    unique_flights = []
    for f in flights:
        if f not in unique_flights:
            unique_flights.append(f)
    
    return f"I TR T {aircraft_suffix} {' '.join(unique_flights)}"

st.set_page_config(page_title="Flight Ops Tool", layout="wide")
st.title("✈️ Flight Operations Formatter")

# --- SECTION 1: ALLOCATION CONVERTER ---
st.header("1. Aircraft Allocation")
uploaded_file = st.file_uploader("Drop your .msg report here", type="msg")

if uploaded_file:
    try:
        msg = extract_msg.Message(uploaded_file)
        result = parse_aircraft_data(msg.body)
        st.success("Allocation String:")
        st.code(result)
    except Exception as e:
        st.error(f"Error processing .msg: {e}")

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
            stn_2 = "" # Not used for DIVT
            
    with col3:
        arr_time = st.text_input("Arrival Time", placeholder="1020")
        reason = st.selectbox("Reason Code", ["WT", "OP", "TD"])

    # This button processes the form
    submit_button = st.form_submit_button("Generate Diversion Message")

# --- Logic to Generate the Output ---
if submit_button:
    if not flight_num or not stn_1 or not arr_time:
        st.warning("Please fill in the Flight Number, Station, and Arrival Time.")
    else:
        if div_type == "Continue (DIVN)":
            # Format: I DIVN BHX-LCY E1020 WT
            final_string = f"I DIVN {stn_1}-{stn_2} E{arr_time} {reason}"
        else:
            # Format: I DIVT BHX E1020 WT
            final_string = f"I DIVT {stn_1} E{arr_time} {reason}"
        
        st.subheader("Generated Message:")
        st.code(final_string)
