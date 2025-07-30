from main import df
import seaborn as sns
import matplotlib.pyplot as plt

# Pairplot - shows relationships between features
sns.pairplot(df, hue='species')
plt.show()
