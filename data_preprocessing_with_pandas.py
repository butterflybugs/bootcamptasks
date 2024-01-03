import requests
import pandas as pd
import numpy as np
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns

url = "https://raw.githubusercontent.com/donde-esta-la-biblioteca/Woolworths-Coles-IGA/main/Data/2021-04-23%20WOW%20Data.csv"

response = requests.get(url)

if response.status_code == 200:
    print(response.text[:200])

    data = pd.read_csv(StringIO(response.text))

    print("\nOriginal Data Types:")
    print(data.dtypes)

    # Convert categorical columns to category type
    categorical_columns = ['Brand', 'Product Name', 'Specials', 'Tag Description', 'Online Only', 'New Product', 'Ratings', 'Department', 'Product URL']
    data[categorical_columns] = data[categorical_columns].astype('category')

    # Convert numeric columns to appropriate types and impute missing values
    numeric_columns = ['SKU', 'Price', 'Package Size', 'Price per unit']
    data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # Impute missing values in numeric columns with the mean
    data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].mean())

    data['Availability'] = data['Availability'].astype('category')
    data['Ratings'] = pd.to_numeric(data['Ratings'], errors='coerce')
    data['Date'] = pd.to_datetime(data['Date'])

    print("\nUpdated Data Types:")
    print(data.dtypes)

    print("\nProduct Names for Available Products:")
    print("\nProduct Names for the First 10 Available Products:")
    counter = 0
    # loops over the data and returns the first 10 available products
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

    # summary of the DataFrame
    print("\nDataFrame Information:")
    print(data.info())

    # descriptive statistics for numeric columns
    print("\nSummary Statistics for Numeric Columns:")
    print(data.describe())

    # Find and remove duplicates
    duplicate_rows = data[data.duplicated()]
    print("\nDuplicate Rows:")
    print(duplicate_rows)

    data = data.drop_duplicates()
    print("\nDataFrame after removing duplicates:")
    print(data)

    # Use groupby to find total and average prices per category/ies
    category_prices = data.groupby('Department')['Price'].agg(['sum', 'mean'])
    print("\nTotal and Average Prices per Category:")
    print(category_prices)

    # Create a column called "quantity" with random numbers from Numpy
    np.random.seed(42)  # Set seed for reproducibility
    data['Quantity'] = np.random.randint(1, 100, size=len(data))

    # Correlation analysis on Price, Quantity, and Ratings
    numeric_columns = ['Price', 'Quantity', 'Ratings']
    correlation_matrix = data[numeric_columns].corr()
    print("\nCorrelation Analysis:")
    print(correlation_matrix)


# Visualizations

# Histogram of Product Prices
plt.figure(figsize=(12, 6))
plt.hist(data['Price'].dropna(), bins=50, color='skyblue', edgecolor='black', alpha=0.7)
plt.title('Distribution of Product Prices')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()

# Histogram of Product Quantities
plt.figure(figsize=(12, 6))
plt.hist(data['Quantity'].dropna(), bins=50, color='lightcoral', edgecolor='black', alpha=0.7)
plt.title('Distribution of Product Quantities')
plt.xlabel('Quantity')
plt.ylabel('Frequency')
plt.show()

# Bar Chart of Total and Average Prices per Department
department_prices = data.groupby('Department')['Price'].agg(['sum', 'mean'])
department_prices.plot(kind='bar', figsize=(14, 7), color=['lightgreen', 'lightblue'])
plt.title('Total and Average Prices per Department')
plt.xlabel('Department')
plt.ylabel('Price')
plt.legend(['Total Price', 'Average Price'])
plt.show()

# Correlation Matrix Heatmap
correlation_matrix = data[['Price', 'Quantity', 'Ratings']].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5)
plt.title('Correlation Matrix Heatmap')
plt.show()

print("\n My analysis on what I have observed so far:")
print("\nI have performed a comprehensive exploration of a dataset containing information about various products, ranging from their brands and prices to availability and department categorization. Leveraging Python's pandas library, I initially examined the data's structure, identifying and converting columns to appropriate data types. Further, I conducted data cleaning by addressing missing values and duplicates, ensuring the dataset's integrity. Utilizing the groupby() function, I computed total and average prices per department, providing insights into the pricing distribution across different product categories. Additionally, I introduced a 'Quantity' column with random values and conducted a correlation analysis, revealing the relationships between price, quantity, and ratings. ")