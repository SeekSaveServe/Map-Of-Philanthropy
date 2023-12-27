import pandas as pd

# Step 2: Read the Excel file
file_path = 'to_fix.xlsx'
df = pd.read_excel(file_path)

classification = {
    "Arts and Heritage": [
        "Historical & Cultural Conservation", "Literary Arts", "Music & Orchestras",
        "Professional, Contemporary & Ethnic Dance", "Theatre & Dramatic Arts",
        "Traditional Ethnic Performing Arts", "Training & Education", "Others", "Visual Arts"
    ],
    "Community": [
        "Others", "South East", "South West", "North East", "North West", "Central"
    ],
    "Education": [
        "Local Educational Institutions/Funds", "Independent Schools",
        "Foreign Educational Institutions/Funds", "Foundations & Trusts",
        "Government-Aided Schools", "Others", "Uniformed Groups"
    ],
    "Health": [
        "TCM C", "Others", "Palliative Home Care", "Health Professional Group",
        "Home Care", "Hospital/Statutory Board", "Renal Dialysis", "Active Ageing",
        "Mental Health", "Cluster/Hospital Funds", "Other Community-based Services",
        "Trust/Research Funds", "Hospice", "Nursing Home", "Community/Chronic Sick Hospital",
        "Day Rehabilitation Centre", "Diseases/Illnesses Support Group"
    ],
    "Others": [
        "Environment", "Children/Youth", "Animal Welfare", "Humanitarian Aid",
        "General Charitable Purposes", "Think Tanks", "Self-Help Groups", "Others"
    ],
    "Religious": [
        "Others", "Taoism", "Hinduism", "Islam", "Buddhism", "Christianity"
    ],
    "Social and Welfare": [
        "Community", "Children/Youth", "Family", "Eldercare", "Disability(Adult)",
        "Disability(Children)", "Support Groups", "Others"
    ],
    "Sports": [
        "Trust Funds", "Youth Sports", "Disability Sports", "Competitive Sports",
        "Others", "NSAs", "Mind Sports", "Non-NSAs"
    ]
}

activities = classification.items()
print(df.dtypes)
if df['Sector'].dtype != 'object':
    df['Sector'] = df['Sector'].astype(str)
# Step 3: Iterate through each row
for index, row in df.iterrows():
    # Step 4: Process the content of each line
    # Example: If a certain condition is met in column 'A', update column 'B'
    for sector, subsectors in activities:
        try:
            if pd.isna(row['Classification']):
                df.at[index, 'Sector'] = 'Unclassified'
                continue
            for classifier in row['Classification'].split(';'):
                if classifier == 'Diseases/Illnessess Support Group':
                    df.at[index, 'Sector'] = 'Health'
                    continue
                if classifier in subsectors:
                    # print(classifier, subsectors, sector)
                    df.at[index, 'Sector'] = sector
                    break
        except AttributeError:
            print(row)
            raise AttributeError
# Step 6: Save the modified DataFrame
df.to_excel(file_path, index=False)
