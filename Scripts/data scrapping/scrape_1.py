import requests
import pandas as pd
import itertools

# Defining the possible values for each input field
activities = [
    "Direct Services", "Research", "Financial assistance, bursaries & scholarships",
    "Supports other Charities", "Grantmaking", "Training & education",
    "Public awareness, promotion & advisory"
]

financial_size = [
    "$0", "$50,000 and <$200,000", "$200,000 and <$250,000", 
    "$250,000 and <$500,000", "$500,000 and <$1,000,000", 
    "$1,000,000 and <$5,000,000", "$5,000,000 and <$10,000,000", "$10,000,000"
]

primary_sector = [
    "Arts and Heritage", "Community", "Education", "Health", "Others", 
    "Religious", "Social and Welfare", "Sports"
]

status_of_charity = [
    "Institutions of a Public Character (IPCs)", "De-registered Charities", 
    "Exempt Charities", "De-exempted Charities"
]

# For simplicity, we'll just use a few classifications for now
classification = {
    "Arts and Heritage": [
        "Historical & Cultural Conservation", "Literary Arts", "Music & Orchestras",
        "Professional, Contemporary & Ethnic Dance", "Theatre & Dramatic Arts",
        "Traditional Ethnic Performing Arts", "Training & Education", "Others", "Visual Arts"
    ],
    # Add other sectors if needed
}

# Generating all combinations
combinations = list(itertools.product(activities, [i for i in range(len(financial_size))], primary_sector, status_of_charity))

# Just to see the number of combinations and a few examples
# Base URL
base_url = "https://www.charities.gov.sg/_layouts/15/CPInternet/AdvanceSearchHandler.ashx"

# Placeholder for results
results = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
# Iterate over a subset of combinations for testing
total = len(combinations)
for activity, fin_size, sector, status in combinations:
    print("Progress: {}/{}".format(len(results), total)) 
    # Construct query parameters
    params = {
        "query": f"?advType=0&financialSize={fin_size}",  # This is just a basic structure, adjust as needed
        "reqType": "charityInfo",
        "filterColumn": ""
    }
    # Make the request
    response = requests.get(base_url, params=params, headers=headers)
    
    # Check if the response is valid
    if response.status_code == 200:
        # print(response.text)
        data = response.json()
        # Extract relevant data from response (this needs to be adjusted based on actual response structure)
        for item in data['charityInfosData']:  # Assuming 'data' key contains the results
            results.append({
                "Charity/IPC Name": item.get("CharityIPCName", ""),
                "UENNo": item.get("UENNo", ""),
                "Sector Administrator": item.get("SectorAdministrato", ""),
                "Activities": item.get("Activities", ""),
                "Registration Date": item.get("RegistrationDate", ""),
                "Input Activity": activity,
                "Input Financial Size": fin_size,
                "Input Sector": sector,
                "Input Status": status
            })

# Convert results to DataFrame
df_results = pd.DataFrame(results)

# Save the DataFrame to an Excel file
df_results.to_excel("output_data.xlsx", index=False)