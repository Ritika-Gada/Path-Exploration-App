import os

def load_onet_data(base_dir="onet_data/db_30_3_text"):
    """
    Parses O*NET 30.3 database text files:
    - Occupation Data.txt (for SOC code, Title, and Description)
    - Career Interest Types.txt (for RIASEC Element values on Scale ID 'OI', rescaled to 0-10)
    
    Returns:
        dict: { soc_code: { 'title': str, 'description': str, 'riasec': { 'R': float, ... } } }
    """
    occ_file = os.path.join(base_dir, "Occupation Data.txt")
    interest_file = os.path.join(base_dir, "Career Interest Types.txt")
    
    # 1. Parse Occupation Data
    occupations = {}
    if not os.path.exists(occ_file):
        raise FileNotFoundError(f"Occupation Data file not found at: {occ_file}")
        
    with open(occ_file, "r", encoding="utf-8") as f:
        # Read header
        header = f.readline().strip().split("\t")
        for line in f:
            parts = line.strip("\r\n").split("\t")
            if len(parts) >= 2:
                soc_code = parts[0]
                title = parts[1]
                description = parts[2] if len(parts) >= 3 else ""
                occupations[soc_code] = {
                    "title": title,
                    "description": description,
                    "riasec": {dim: 5.0 for dim in ["R", "I", "A", "S", "E", "C"]} # default 5.0
                }
                
    # 2. Parse Career Interest Types (RIASEC values)
    if not os.path.exists(interest_file):
        raise FileNotFoundError(f"Career Interest Types file not found at: {interest_file}")
        
    with open(interest_file, "r", encoding="utf-8") as f:
        # Read header
        header = f.readline().strip().split("\t")
        for line in f:
            parts = line.strip("\r\n").split("\t")
            if len(parts) >= 5:
                soc_code = parts[0]
                elem_name = parts[2] # Realistic, Investigative, etc.
                scale_id = parts[3]  # OI, IH
                data_val = parts[4]
                
                # Only look at Occupational Interest (OI)
                if scale_id == "OI":
                    dim_char = elem_name[0].upper() # R, I, A, S, E, C
                    if dim_char in ["R", "I", "A", "S", "E", "C"]:
                        try:
                            val = float(data_val)
                            # Linear rescale: [1.0, 7.0] -> [0.0, 10.0]
                            rescaled = (val - 1.0) / 6.0 * 10.0
                            # Clamp just in case of slight precision anomalies
                            rescaled = max(0.0, min(10.0, rescaled))
                            rescaled = round(rescaled, 2)
                            
                            if soc_code in occupations:
                                occupations[soc_code]["riasec"][dim_char] = rescaled
                        except ValueError:
                            pass
                            
    return occupations

if __name__ == "__main__":
    # Self-test loader
    try:
        data = load_onet_data()
        print(f"Loaded {len(data)} occupations successfully.")
        # Check Data Scientists mapping
        ds = data.get("15-2051.00")
        if ds:
            print("15-2051.00 Data Scientists interest values:", ds["riasec"])
        else:
            print("15-2051.00 not found in database.")
    except Exception as e:
        print(f"Error testing loader: {e}")
