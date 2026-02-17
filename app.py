import streamlit as st
import extract_msg
import re

def parse_aircraft_data(text):
    # Extracts the last 3 letters of the registration (e.g., CAD)
    reg_match = re.search(r'G-LC([A-Z]{2})', text)
    aircraft_suffix = reg_match.group(1) if reg_match else "CAD"
    
    # Extracts flight numbers by removing 'BA' prefix
    flights = re.findall(r'BA(\d{1,4}[A-Z]?)', text)
    
    # Keeps unique flight numbers in order
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
        st.success("Allocation String Generated:")
        st.code(result)
    except Exception as e:
        st.error(f"Error: {e}")

st.divider()

# --- SECTION 2: DIVERSION BOX ---
st.header("2. Diversion")
with st.expander("Open Diversion Input", expanded=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        div_type = st.selectbox("Type", ["DIVN (Continue)", "DIVT (Terminate)"])
        flight_num = st.text_input("Flight Number", placeholder="e.g. 8465")
    
    with col2:
        if div_type == "DIVN (Continue)":
            stn_1 = st.text_input("Diversion Station", placeholder="BHX")
            stn_2 = st.text_input("Next Station", placeholder="LCY")
            station_string = f"{stn_1}-{stn_2}"
            prefix = "I DIVN"
        else:
            stn_1 = st.text_input("Terminate Station", placeholder="BHX")
            station_string = stn_1
            prefix = "I DIVT"
            
    with col3:
        arr_time = st.text_input("Arrival Time", placeholder="1020")
        reason = st.selectbox("Reason", ["WT", "OP", "TD"])

    # Generate Diversion Output
    if flight_num and stn_1 and arr_time:
        div_output = f"{prefix} {station_string} E{arr_time} {reason}"
        st.info("Diversion String Generated:")
        st.code(div_output)
