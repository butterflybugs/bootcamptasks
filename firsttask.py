import requests
import pandas as pd 
from io import StringIO

url = "https://raw.githubusercontent.com/donde-esta-la-biblioteca/Woolworths-Coles-IGA/main/Data/2021-04-23%20WOW%20Data.csv"

response = requests.get(url)

if response.status_code ==200:
    print(response.text[:200])

    data = pd.read_csv(StringIO(response.text))
    print(data.head())
else:
    print(f"failed to fetch data")