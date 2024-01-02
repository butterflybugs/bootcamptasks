import requests
import pandas as pd
from io import StringIO
from typing import Tuple


def display_overview(data: pd.DataFrame) -> None:
    print("\nDataFrame Overview:")
    print(data.info())


def summary_statistics(data: pd.DataFrame) -> pd.DataFrame:
    return data.describe().transpose()

def display_unique_values(data: pd.DataFrame, categorical_columns: list) -> None:
    print("\nUnique Values in Categorical Columns:")
    for col in categorical_columns:
        print(f"{col}: {data[col].unique()}")


def most_bought_product(data: pd.DataFrame) -> Tuple[str, int]:
    most_bought_product = data['Product Name'].value_counts().idxmax()
    most_bought_count = data['Product Name'].value_counts().max()
    return most_bought_product, most_bought_count


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
    counter = 0
    for index, row in data.iterrows():
        if row['Availability'] == 'Available':
            print(row['Product Name'])
            counter += 1

            if counter == 10:
                break

    else:
        print(f"Failed to fetch data")

    # Display overview
    display_overview(data)

    #  summary statistics
    summary_stats = summary_statistics(data)
    print("\nSummary Statistics for Numeric Columns:")
    print(summary_stats)

    display_unique_values(data, categorical_columns)

    #bought product
    most_bought, count = most_bought_product(data)
    print(f"\nThe most bought product is '{most_bought}' with a count of {count}.")

else:
    print(f"Failed to fetch data")