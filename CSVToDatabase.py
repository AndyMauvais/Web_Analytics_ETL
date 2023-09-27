# Web Analytics ETL

# Import Libraries
import sqlite3
import pandas as pd
import csv

# Connect to SQLite Database (if file doesnt exist, SQLIte will create it)
# conn = sqlite3.connect("web_analytics.db")

# Load data
csv_file = "Data/Web_Analytics_Dataset.csv"
df = pd.read_csv(csv_file)


# Clean and Transform any data.
# ...the data is mostly clean.

#Changing Conversion Rate column to include %'s similar to [bounce rate]
df = df.rename(columns={"Conversion Rate (%)": "Conversion Rate"})

## Convert the column to numeric, instead of ignoring errors, decided to set to NaN
df['Conversion Rate'] = pd.to_numeric(df['Conversion Rate'], errors='coerce')
df['Conversion Rate'] = (df['Conversion Rate'] * 100).round(2)

# Function to update values with %
def update_percentage(value):
    # Check if the value is numeric
    if isinstance(value, (int, float)):
        # If numeric, convert to string and concatenate '%'
        return str(value) + '%'
    else:
        # If not numeric, return the value as is
        return value

# Update the column
df['Conversion Rate'] = df['Conversion Rate'].apply(update_percentage)


## Check for unexpected values in the 'Conversion Rate' column
#unexpected_values = df[df['Conversion Rate'].apply(lambda x: not isinstance(x, (int, float)))]
#print("Unexpected Values:")
#print(unexpected_values)


# connect to db
conn = sqlite3.connect("web_analytics.db")

# export csv to sql
df.to_sql("Web_Analytics1", conn, if_exists="replace", index=False)

# export sql to csv
cursor = conn.cursor()
cursor.execute("SELECT * FROM Web_Analytics1")
data = cursor.fetchall()

## Write to CSV
csv_filename = "Data/transformed_web_analytics.csv"
with open(csv_filename, "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    
    header = df.columns.tolist() #DataFrame column headers

    csv_writer.writerow(header)
    #Write Data
    csv_writer.writerows(data)

conn.close
