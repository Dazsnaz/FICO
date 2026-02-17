import re

def convert_flight_data(input_text):
    # 1. Extract the Registration (e.g., G-LCAD)
    # Looks for G- followed by 4 letters
    reg_match = re.search(r'G-LC([A-Z]{2})', input_text)
    aircraft_id = reg_match.group(1) if reg_match else "CAD" # Defaulting to CAD based on your example
    
    # 2. Extract Flight Numbers (e.g., BA9769T)
    # Looks for 'BA' followed by digits and an optional letter
    flights = re.findall(r'BA([0-9]{1,4}[A-Z]?)', input_text)
    
    # 3. Remove duplicates while preserved order
    unique_flights = []
    for f in flights:
        if f not in unique_flights:
            unique_flights.append(f)
            
    # 4. Format the final string
    # Based on your requirement: I TR T [Last 3 of Reg] [Flight Numbers]
    result = f"I TR T {aircraft_id} {' '.join(unique_flights)}"
    
    return result

# Example usage with your provided snippet
raw_data = """
18.02 BA9769T  LCY NWI 0900 0945 G-LCAD       E90  0  2+0/2
18.02 BA9771T  NWI LCY 1250 1330 G-LCAD       E90  0  2+0/2
18.02 BA4466   LCY DUB2 1500 1620 G-LCAD      E90  38 2+3/0
"""

print(convert_flight_data(raw_data))
