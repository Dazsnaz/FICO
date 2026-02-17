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

st.title("✈️ Aircraft Allocation Formatter")

uploaded_file = st.file_uploader("Drop your .msg report here", type="msg")

if uploaded_file:
    msg = extract_msg.Message(uploaded_file)
    # The 'body' contains the flight details like BA9769T and G-LCAD 
    result = parse_aircraft_data(msg.body)
    st.subheader("System Input String:")
    st.code(result)
