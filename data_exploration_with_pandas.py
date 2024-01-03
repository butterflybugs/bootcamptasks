import requests
import pandas as pd
from io import StringIO

url = "https://raw.githubusercontent.com/donde-esta-la-biblioteca/Woolworths-Coles-IGA/main/Data/2021-04-23%20WOW%20Data.csv"

response = requests.get(url)

if response.status_code == 200:
    print(response.text[:200])

    data = pd.read_csv(StringIO(response.text))

    print("\nOriginal Data Types:")
    print(data.dtypes)

    categorical_columns = ['Brand', 'Product Name', 'Specials', 'Tag Description', 'Online Only', 'New Product', 'Ratings', 'Department', 'Product URL']
    data[categorical_columns] = data[categorical_columns].astype('category')

    numeric_columns = ['SKU', 'Price', 'Package Size', 'Price per unit']
    data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')

    data['Availability'] = data['Availability'].astype('category')

    data['Date'] = pd.to_datetime(data['Date'])

    print("\nUpdated Data Types:")
    print(data.dtypes)

    print("\nProduct Names for Available Products:")
    print("\nProduct Names for the First 10 Available Products:")
counter = 0
#loops over the data and returns the first 10 available products
for index, row in data.iterrows():
        if row['Availability'] == 'Available':
            print(row['Product Name'])
            counter += 1

            if counter == 10:
                break

else:
    print(f"Failed to fetch data")

available_products = data[data['Availability'] == 'Available']
print(f"\nNumber of Available Products: {len(available_products)}")
# Display the first rows 
print("\nFirst Few Rows of the DataFrame:")
print(data.head())

#  summary of the DataFrame
print("\nDataFrame Information:")
print(data.info())

# descriptive statistics for numeric columns
print("\nSummary Statistics for Numeric Columns:")
print(data.describe())
