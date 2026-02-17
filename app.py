import streamlit as st
import extract_msg
import re
from collections import defaultdict

def process_multi_aircraft(text):
    # Dictionary to hold: { "CAD": ["9769T", "9771T"], "CAE": ["8822", "8823"] }
    allocation = defaultdict(list)
    
    # Split text into individual lines to keep data paired correctly
    lines = text.split('\n')
    
    for line in lines:
        # Find the Registration (e.g., G-LCAD)
        reg_match = re.search(r'G-LC([A-Z]{2})', line)
        # Find the Flight Number (e.g., BA9769T)
        flight_match = re.search(r'BA(\d{1,4}[A-Z]?)', line)
        
        if reg_match and flight_match:
            suffix = reg_match.group(1)
            flight_num = flight_match.group(1)
            # Add flight to that specific aircraft's list if not already there
            if flight_num not in allocation[suffix]:
                allocation[suffix].append(flight_num)
    
    # Build the final multi-line string
    output_lines = []
    for suffix, flights in allocation.items():
        flight_str = " ".join(flights)
        output_lines.append(f"I TR T {suffix} {flight_str}")
    
    return "\n".join(output_lines)

st.title("✈️ Multi-Aircraft Formatter")

uploaded_file = st.file_uploader("Upload .msg report", type="msg")

if uploaded_file:
    msg = extract_msg.Message(uploaded_file)
    final_result = process_multi_aircraft(msg.body)
    
    st.subheader("System Input:")
    # Using st.text so it preserves the new lines clearly
    st.text(final_result)
    
    # Easy copy button for the whole block
    st.download_button("Download as Text File", final_result, file_name="allocation.txt")
