import pandas as pd

# Import the CSV file
file_path = 'vehicles_us.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the dataset
print(data.head())
