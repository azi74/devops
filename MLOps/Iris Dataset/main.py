from sklearn.datasets import load_iris
import pandas as pd

# Load the iris dataset
data = load_iris()

# Convert to pandas DataFrame
df = pd.DataFrame(data.data, columns=data.feature_names)
df['species'] = data.target

# Show first few rows
print(df.head())
