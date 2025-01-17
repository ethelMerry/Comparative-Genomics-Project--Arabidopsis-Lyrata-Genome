'''
##THIS IS FOR HISTOGRAM PLOT OF KS VALUES


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
file_path = "KAKS/final_KSfiltered_file.csv"  # Update with your actual file path
df = pd.read_csv(file_path, header=None)  # Assuming no header in the file

# Extract the Ks values (third column)
ks_values = df[2]

# Plot the histogram
plt.figure(figsize=(8, 5))
sns.histplot(ks_values, bins=50, kde=True, color='blue')

# Labels and title
plt.xlabel("Ks Values")
plt.ylabel("Frequency")
plt.title("Histogram of Ks Values")
plt.grid(True)

# Show the plot
plt.show()
'''

##THIS IS FOR THE DENSITY AND BOX PLOTS OF KS VALUES WITH THE TAG STATUS

import pandas as pd

# Load the data from the CSV file
data = pd.read_csv("KAKS/annotated_ks1.csv")

# Check the first few rows to ensure it's loaded correctly
print(data.head())

import seaborn as sns
import matplotlib.pyplot as plt

# Set the color palette
sns.set_palette("Set2")

# Create the density plot
plt.figure(figsize=(10, 6))
sns.kdeplot(data=data, x="Ks", hue="Tag_Status", fill=True, common_norm=False)

# Add titles and labels
plt.title("Density Plot of Ks Values for Tag and Non-Tag Pairs", fontsize=16)
plt.xlabel("Ks Value", fontsize=12)
plt.ylabel("Density", fontsize=12)

# Create the box plot
plt.figure(figsize=(8, 6))
sns.boxplot(x="Tag_Status", y="Ks", data=data, palette="Set2")

# Add titles and labels
plt.title("Box Plot of Ks Values for Tag and Non-Tag Pairs", fontsize=16)
plt.xlabel("Tag Status", fontsize=12)
plt.ylabel("Ks Value", fontsize=12)

# Display the plot
plt.show()

