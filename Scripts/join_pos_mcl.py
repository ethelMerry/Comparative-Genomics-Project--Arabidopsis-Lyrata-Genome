import pandas as pd

# Load the files with correct delimiters
file1 = pd.read_csv("./new MCL/genes_positions.csv", sep=',')  # Comma-separated for file1
file2 = pd.read_csv("./new MCL/low_gene_family.tsv", sep='\t')  # Tab-separated for file2

# Merge data on the 'gene_id' column using left join to keep unmatched entries
merged_df = file1.merge(file2, on="gene_id", how="left")

# Remove decimal points in the 'Family' column if present
merged_df['Family'] = merged_df['Family'].fillna('').astype(str).str.replace(r'\.0$', '', regex=True)

# Fill missing values in 'Family' column with 'non_associated'
merged_df['Family'] = merged_df['Family'].replace('', 'N/A')

# Save the modified data to a new .tsv file
merged_df.to_csv("LOW_merged_fam.tsv", sep='\t', index=False)

print("Merge completed, decimal points removed, and missing values in 'Family' replaced with 'N/A'.")
