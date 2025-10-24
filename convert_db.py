import pandas as pd
import sqlite3

# --- 1. Load Data ---
project_df = pd.read_csv('data/project.csv')
address_df = pd.read_csv('data/ProjectAddress.csv')
configuration_df = pd.read_csv('data/ProjectConfiguration.csv')
variant_df = pd.read_csv('data/ProjectConfigurationVariant.csv')

# --- 2. Rename Columns ---
project_df = project_df.rename(columns={'id': 'projectId'})
configuration_df = configuration_df.rename(columns={'id': 'configurationId'})
variant_df = variant_df.rename(columns={'id': 'variantId'})
address_df = address_df.rename(columns={'id': 'addressId'})

# --- 3. Merge Operations ---
# Merge 1: Project and Address
df_pa = pd.merge(
    project_df,
    address_df,
    on='projectId',
    how='left',
    suffixes=('_P', '_A')
)

# Merge 2: Configuration and Variant
df_cv = pd.merge(
    configuration_df,
    variant_df,
    on='configurationId',
    how='left',
    suffixes=('_C', '_V')
)

# Merge 3: Master Table (PA) and (CV)
df_master = pd.merge(
    df_pa,
    df_cv,
    on='projectId',
    how='left',
    suffixes=('_PA', '_CV')
)

# --- 4. Select and Format Columns ---
final_columns = [
    'projectId', 'projectName', 'status', 'slug', 'possessionDate',
    'configurationId', 'type', 'customBHK',
    'fullAddress', 'pincode', 'landmark',
    'variantId', 'carpetArea', 'price', 'bathrooms', 'balcony',
    'furnishedType', 'listingType', 'lift', 'propertyImages', 'aboutProperty',
]

df_master = df_master[final_columns]

# Function to format price into Cr or L
def format_price(price):
    if pd.isna(price):
        return None
    price = int(price)
    if price >= 10000000:
        return f"₹{price / 10000000:.2f} Cr"
    elif price >= 100000:
        return f"₹{price / 100000:.2f} L"
    return f"₹{price}"

df_master['price_formatted'] = df_master['price'].apply(format_price)

# --- 5. Save to SQLite Database ---
db_file = 'database/nobrokerage_properties.db'
table_name = 'properties'

# Create a connection and save the DataFrame to the database
conn = sqlite3.connect(db_file)
df_master.to_sql(table_name, conn, if_exists='replace', index=False)
conn.close()

print(f"Successfully saved the master property data to the SQLite database: {db_file}")
print(f"The data is available in the table: {table_name}")