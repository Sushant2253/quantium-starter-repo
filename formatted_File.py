import pandas as pd
import os

# Path to the data folder
data_folder = "data"

# List all CSV files in the data folder
csv_files = [file for file in os.listdir(data_folder) if file.endswith('.csv')]

# Initialize an empty DataFrame to store combined data
combined_data = pd.DataFrame()

if not csv_files:
    print("No CSV files found in the data folder!")

# Process each CSV file
for csv_file in csv_files:
    # Load the CSV file into a DataFrame
    file_path = os.path.join(data_folder, csv_file)
    print(f"Processing file: {file_path}")
    
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        continue
    
    # Print first few rows to verify the data
    print(df.head())

    # Filter rows where product is "Pink Morsels" (case-insensitive)
    df = df[df['product'].str.lower() == 'pink morsel']
    print(f"Filtered rows: {len(df)}")

    # Create the "sales" field by multiplying "quantity" and "price"
    # Remove the dollar sign and convert to numeric
    df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)
    df['sales'] = df['quantity'] * df['price']
    
    # Keep only the required columns: "sales", "date", and "region"
    df = df[['sales', 'date', 'region']]
    
    # Append to the combined DataFrame
    combined_data = pd.concat([combined_data, df], ignore_index=True)

# Check if combined_data has rows
if combined_data.empty:
    print("No data found after processing. Check the input files and filters.")
else:
    # Save the combined data to a new CSV file
    output_file = "formatted_output.csv"
    combined_data.to_csv(output_file, index=False)
    print(f"Formatted data has been saved to {output_file}")
