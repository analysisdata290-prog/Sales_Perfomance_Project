import pandas as pd
import requests
from supabase import create_client
from io import StringIO
import os
from datetime import datetime

# ================== CONFIGURATION ==================
# Supabase Config (Environment Variables)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Google Sheet Config (Environment Variables)
SHEET_ID = os.getenv("SALES_SHEET_ID")

# ================== FUNCTION TO LOAD SHEET ==================
def load_sheet(sheet_name, skiprows=None, usecols=None):
    """
    Load a Google Sheet by name using the export URL
    """
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&sheet={sheet_name}"
    response = requests.get(url)
    response.raise_for_status()
    
    if skiprows is not None:
        return pd.read_csv(StringIO(response.text), skiprows=skiprows, usecols=usecols)
    return pd.read_csv(StringIO(response.text))

# ================== LOAD DATA ==================
print("📥 Loading data from Google Sheets...")

# 1. Load Summary Data (Weekly)
df_summary = load_sheet("Summary", skiprows=1, usecols=range(10))
print(f"✅ Loaded Summary Data: {len(df_summary)} rows")

# 2. Load Annual Map (Daily)
df_annual = load_sheet("Annual Map", skiprows=126, usecols=range(9))
print(f"✅ Loaded Annual Map: {len(df_annual)} rows")

# ================== CLEAN COLUMN NAMES ==================
def clean_cols(df):
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace('/', '_')
    df.columns = df.columns.str.replace('-', '_')
    df.columns = df.columns.str.replace('(', '')
    df.columns = df.columns.str.replace(')', '')
    df.columns = df.columns.str.replace('SAR', '')
    df.columns = df.columns.str.replace(',', '')
    return df

df_summary = clean_cols(df_summary)
df_annual = clean_cols(df_annual)

# ================== REMOVE EMPTY ROWS ==================
df_summary = df_summary.dropna(how='all')
df_annual = df_annual.dropna(how='all')

print(f"\n📊 After cleaning:")
print(f"   Summary: {len(df_summary)} rows")
print(f"   Annual: {len(df_annual)} rows")

# ================== COLUMN MAPPING ==================
# Mapping for Summary table
summary_mapping = {
    'Date': 'date_range',
    'Total_Sales_Value': 'total_sales_value',
    'No_of_Customers': 'no_of_customers',
    'No_of_Data_Customers': 'no_of_data_customers',
    'No_of_Leads_Customers': 'no_of_leads_customers',
    'Data_Sales_Volume': 'data_sales_volume',
    'Leads_Sales_Volume': 'leads_sales_volume',
    'Next_Week_Sales_Forecast': 'next_week_sales_forecast',
    'No_of_Data_Meetings': 'no_of_data_meetings',
    'No_of_Leads_Meetings': 'no_of_leads_meetings'
}

# Mapping for Annual Map table
annual_mapping = {
    'Date': 'date',
    'Daily_Contacts': 'daily_contacts',
    'Leads': 'leads',
    'Meetings': 'meetings',
    'Meetings_Done': 'meetings_done',
    'Contracts': 'contracts',
    'Contracts_Value': 'contracts_value',
    'Paid_Clients': 'paid_clients',
    'Total_Sales': 'total_sales'
}

# ================== UPLOAD TO SUPABASE ==================
def upload_to_supabase(df, table_name, column_mapping, batch_size=500):
    """
    Upload DataFrame to Supabase in batches
    """
    # Rename columns based on mapping
    df_renamed = df.rename(columns=column_mapping)
    
    # Keep only columns that exist in the mapping
    df_renamed = df_renamed[list(column_mapping.values())]
    
    total_rows = len(df_renamed)
    if total_rows == 0:
        print(f"⚠️ No data to upload to {table_name}")
        return
    
    print(f"\n📤 Uploading {total_rows} rows to {table_name}...")
    
    for i in range(0, total_rows, batch_size):
        batch = df_renamed.iloc[i:i+batch_size].to_dict(orient='records')
        try:
            supabase.table(table_name).insert(batch).execute()
            print(f"   ✅ Uploaded rows {i+1} to {min(i+batch_size, total_rows)}")
        except Exception as e:
            print(f"   ❌ Error uploading batch: {e}")
    
    print(f"✅ Done uploading to {table_name}")

# ================== UPLOAD TO TABLES ==================
# Upload to Summary table
upload_to_supabase(df_summary, 'summary', summary_mapping)

# Upload to Annual Map table
upload_to_supabase(df_annual, 'annual_map', annual_mapping)

# ================== VERIFY UPLOAD ==================
print("\n🔍 Verifying upload...")

def verify_upload(table_name):
    result = supabase.table(table_name).select("*", count="exact").execute()
    count = result.count
    print(f"   {table_name}: {count} rows")

verify_upload('summary')
verify_upload('annual_map')

print("\n✅ All data uploaded successfully!")
