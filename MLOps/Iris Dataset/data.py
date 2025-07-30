from main import df

# Check shape (rows, columns)
print(df.shape)

# Summary stats
print(df.describe())

# Count of each class
print(df['species'].value_counts())

# Check for missing values
print(df.isnull().sum())
