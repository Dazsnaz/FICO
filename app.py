import streamlit as st
import extract_msg
import re
from collections import defaultdict

def process_multi_aircraft(text):
    # Dictionary to hold: { "CAD": ["9769T", "9771T"], "CAE": ["8822"] }
    allocation = defaultdict(list)
    
    # Split text into lines to keep flight numbers with their specific aircraft 
    lines = text.split('\n')
    
    for line in lines:
        # 1. Find the Registration (e.g., G-LCAD or G-BAAD) 
        # This looks for 'G-' followed by any 4-5 letters
        reg_match = re.search(r'G-[A-Z]{2,3}([A-Z]{2,3})', line)
        
        # 2. Find the Flight Number (e.g., BA9769T) 
        flight_match = re.search(r'BA(\d{1,4}[A-Z]?)', line)
        
        if reg_match and flight_match:
            # Take the last 3 characters from the registration match
            full_reg = reg_match.group(0) # e.g. G-LCAD
            suffix = full_reg[-3:]        # e.g. CAD
            
            flight_num = flight_match.group(1)
            
            # Add to list if not a duplicate for that specific tail
            if flight_num not in allocation[suffix]:
                allocation[suffix].append(flight_num)
    
    # Format the multi-line output
    output_lines = []
    for suffix, flights in allocation.items():
        flight_str = " ".join(flights)
        output_lines.append(f"I TR T {suffix} {flight_str}")
    
    return "\n".join(output_lines)

# --- Streamlit Interface ---
st.title("✈️ Tail-Specific Flight Formatter")
st.write("Extracts last 3 of REG and groups all flights by aircraft.")

uploaded_file = st.file_uploader("Upload .msg report", type="msg")

if uploaded_file:
    try:
        msg = extract_msg.Message(uploaded_file)
        final_result = process_multi_aircraft(msg.body)
        
        if final_result:
            st.subheader("System Input:")
            st.text(final_result)
            st.download_button("Download Text", final_result, file_name="formatted_flights.txt")
        else:
            st.warning("No registration/flight pairs found in this file.")
    except Exception as e:
        st.error(f"Error reading .msg file: {e}")
