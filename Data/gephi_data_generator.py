import pandas as pd


'''
This generates the data for the Gephi graph.
- Nodes List: Charities (input csv)
- Nodes List: Classification (aggregated by financial size)
- Nodes List: Sector (aggregated by financial size)
- Nodes List: Ministries (aggregated by financial size)
- Edge List: Charity <-> classification 
- Edge List: Classification <-> Sector
- Edge List: Sector <-> Ministry
'''

file_path = "Data/Charities.csv"

# Load the Charities data
charities_df = pd.read_csv(file_path)

# Prepare the charity data for processing
# Add new rows by splitting the classification column
charities_df = charities_df.assign(Classification=charities_df['Classification'].str.split(';')).explode('Classification')

# Remove deregistered charities
charities_df = charities_df[charities_df['Charity Status'] != 'Deregistered']

# Process the financial size - take the middle value of the range
financial_sizes = {"$0":0, "$<50,000": 25000, "$50,000 and <$200,000": 125000, "$200,000 and <$250,000": 225000, "$250,000 and <$500,000": 375000, "$500,000 and <$1,000,000": 750000, "$1,000,000 and <$5,000,000": 3000000, "$5,000,000 and <$10,000,000": 7500000, "$10,000,000": 10000000}
charities_df['Financial Size'] = charities_df['Financial Size'].map(financial_sizes)
charities_df = charities_df.rename(columns={'UENNo': 'Id', 'Charity/IPC Name': 'Label'})
charities_df.to_csv('charities_nodes.csv', index=False)


# Nodes List: Classification (aggregated by financial size)
classification_df = charities_df.groupby(['Classification','Sector'])['Financial Size'].sum().reset_index()
classification_df['Label'] = classification_df['Classification']
classification_df = classification_df.rename(columns={'Classification': 'Id'})
classification_df.to_csv('classification_nodes.csv', index=False)

# Nodes List: Sector (aggregated by financial size)
sector_df = charities_df.groupby('Sector')['Financial Size'].sum().reset_index()
sector_df['Label'] = sector_df['Sector']
sector_df = sector_df.rename(columns={'Sector': 'Id'})
sector_df.to_csv('sector_nodes.csv', index=False)

# Nodes List: Ministries (aggregated by financial size)
ministries_df = charities_df.groupby('Sector Administrator')['Financial Size'].sum().reset_index()
ministries_df['Label'] = ministries_df['Sector Administrator']
ministries_df = ministries_df.rename(columns={'Sector Administrator': 'Id'})
ministries_df.to_csv('ministries_nodes.csv', index=False)

# Edge List: Charity <-> Classification
charity_classification_edges = charities_df[['Id', 'Classification']]
charity_classification_edges = charity_classification_edges.rename(columns={'Classification': 'Target', 'Id': 'Source'})
charity_classification_edges.to_csv('charity_classification_edges.csv', index=False)

# Edge List: Classification <-> Sector
classification_sector_edges = charities_df[['Classification', 'Sector']].drop_duplicates()
classification_sector_edges = classification_sector_edges.rename(columns={'Classification': 'Source', 'Sector': 'Target'})
classification_sector_edges.to_csv('classification_sector_edges.csv', index=False)

# Edge List: Sector <-> Ministry
# Assuming one ministry per sector
sector_ministry_edges = charities_df[['Sector', 'Sector Administrator']].drop_duplicates()
sector_ministry_edges = sector_ministry_edges.rename(columns={'Sector': 'Source', 'Sector Administrator': 'Target'})
sector_ministry_edges.to_csv('sector_ministry_edges.csv', index=False)


