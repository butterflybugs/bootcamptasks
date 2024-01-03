import requests
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# fetch data from  URL and return it as a DataFrame
def fetch_data(url: str) -> pd.DataFrame:
    response = requests.get(url)
    if response.status_code == 200:
        data = pd.read_csv(StringIO(response.text))
        return data
    else:
        print(f"Failed to fetch data")
        return pd.DataFrame()



def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    # Convert numeric columns
    numeric_columns = ['SKU', 'Price', 'Package Size', 'Price per unit']
    data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # Convert categorical columns 
    categorical_columns = ['Brand', 'Product Name', 'Specials', 'Tag Description', 'Online Only', 'New Product', 'Ratings', 'Department', 'Product URL']
    data[categorical_columns] = data[categorical_columns].astype('category')

    # Convert Availability 
    data['Availability'] = data['Availability'].astype('category')

    # ConvertDatecolumn to datetime type
    data['Date'] = pd.to_datetime(data['Date'])

    return data


#
def print_data_types(data: pd.DataFrame) -> None:
    print("\nOriginal Data Types:")
    print(data.dtypes)

    

    print("\nUpdated Data Types:")
    print(data.dtypes)

# Function to display summary statistics for numeric columns
def summary_statistics(data: pd.DataFrame) -> pd.DataFrame:
    return data.describe()

# Function to plot a histogram 
def plot_histogram(data: pd.DataFrame, column: str) -> None:
    data[column].plot(kind='hist', bins=20, edgecolor='black', alpha=0.7)
    plt.title(f'Histogram for {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.show()

# Function to analyze and visualize the distribution of product availability
def availability_analysis(data: pd.DataFrame) -> None:
    availability_counts = data['Availability'].value_counts()
    availability_counts.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Product Availability Distribution')
    plt.xlabel('Availability')
    plt.ylabel('Count')
    plt.show()

# Function to identify and print the top N products based on ratings
def top_rated_products(data: pd.DataFrame, n: int) -> pd.DataFrame:
    top_rated = data.sort_values(by='Ratings', ascending=False).head(n)
    print(f"\nTop {n} Rated Products:")
    print(top_rated[['Product Name', 'Ratings']])
    return top_rated


url = "https://raw.githubusercontent.com/donde-esta-la-biblioteca/Woolworths-Coles-IGA/main/Data/2021-04-23%20WOW%20Data.csv"

# Fetch data
data = fetch_data(url)

if not data.empty:
    # Data preprocessing
    data = preprocess_data(data)

    # data types
    print_data_types(data)

    #  summary statistics
    print("\nSummary Statistics:")
    print(summary_statistics(data))

    # Plot histogram for Price column
    plot_histogram(data, 'Price')
    #visualize product availability distribution
    availability_analysis(data)

    #print top 5 rated products
    top_rated_products(data, 5)

    #printing product names for the first 10 available products
    print("\nProduct Names for the First 10 Available Products:")
    counter = 0
    for index, row in data.iterrows():
        if row['Availability'] == 'Available':
            print(row['Product Name'])
            counter += 1
            if counter == 10:
                break

    #printing the number of available products
    available_products = data[data['Availability'] == 'Available']
    print(f"\nNumber of Available Products: {len(available_products)}")

