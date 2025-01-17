import pandas as pd

# Load the gene data from a TSV file
gene_data = pd.read_csv("./new MCL/sorted_LOW_merged_fam_with_header.tsv", sep="\t", header=None) #change with the high/low data
gene_data.columns = ["gene_id", "chromosome", "start", "end", "strand", "family"]

# Initialize variables for tag identification
tags = []
current_tag = []
current_family = None
spacers_in_tag = 0
genes_in_tag = 0
consecutive_spacers = 0

# Iterate through each gene to identify tags
for idx in range(len(gene_data)):
    row = gene_data.iloc[idx]
    gene_family = row["family"]

    if current_family is None:
        if gene_family != 'non_associated':
            # Start a new tag
            current_family = gene_family
            current_tag = [row]
            genes_in_tag = 1
            spacers_in_tag = 0
            consecutive_spacers = 0
        else:
            # Cannot start a tag with 'non_associated'
            continue
    else:
        if gene_family == current_family:
            # Add gene to current tag
            current_tag.append(row)
            genes_in_tag += 1
            consecutive_spacers = 0
        else:
            # Potential spacer
            if consecutive_spacers >= 1:
                # Cannot have 2 or more spacers in a row, end tag
                if genes_in_tag >= 2:
                    tags.append((current_tag, current_family, spacers_in_tag))
                # Reset variables
                current_family = None
                current_tag = []
                genes_in_tag = 0
                spacers_in_tag = 0
                consecutive_spacers = 0
                # Start a new tag if current gene is not 'non_associated'
                if gene_family != 'non_associated':
                    current_family = gene_family
                    current_tag = [row]
                    genes_in_tag = 1
            else:
                # Check if spacers are less than genes
                if spacers_in_tag < genes_in_tag:
                    # Look ahead to see if there's a gene of the same family ahead
                    has_same_family_ahead = False
                    for next_idx in range(idx + 1, len(gene_data)):
                        next_row = gene_data.iloc[next_idx]
                        next_family = next_row["family"]
                        if next_family == current_family:
                            has_same_family_ahead = True
                            break
                        elif next_family != 'non_associated':
                            # Found gene from a different family
                            break
                    if has_same_family_ahead:
                        # Include as spacer
                        current_tag.append(row)
                        spacers_in_tag += 1
                        consecutive_spacers += 1
                    else:
                        # Cannot continue tag, end tag
                        if genes_in_tag >= 2:
                            tags.append((current_tag, current_family, spacers_in_tag))
                        # Reset variables
                        current_family = None
                        current_tag = []
                        genes_in_tag = 0
                        spacers_in_tag = 0
                        consecutive_spacers = 0
                        # Start a new tag if current gene is not 'non_associated'
                        if gene_family != 'non_associated':
                            current_family = gene_family
                            current_tag = [row]
                            genes_in_tag = 1
                else:
                    # Cannot have spacers equal or more than genes, end tag
                    if genes_in_tag >= 2:
                        tags.append((current_tag, current_family, spacers_in_tag))
                    # Reset variables
                    current_family = None
                    current_tag = []
                    genes_in_tag = 0
                    spacers_in_tag = 0
                    consecutive_spacers = 0
                    # Start a new tag if current gene is not 'non_associated'
                    if gene_family != 'non_associated':
                        current_family = gene_family
                        current_tag = [row]
                        genes_in_tag = 1

# Add the last tag if applicable
if current_tag and genes_in_tag >= 2:
    tags.append((current_tag, current_family, spacers_in_tag))

# Write the output to a file
with open("new MCL/tags_outputLow1.txt", "w") as f: #change path for high/Low data
    for i, (tag_genes, family, spacers) in enumerate(tags):
        chromosome = tag_genes[0]["chromosome"]
        num_genes = len([gene for gene in tag_genes if gene["family"] == family])
        f.write(f"Tag: {i + 1}\n")
        f.write(f"Chromosome: {chromosome}\n")
        f.write(f"Family: {family}\n")
        f.write(f"Number of Genes: {num_genes}\n")
        f.write(f"Number of Spacers: {spacers}\n")
        f.write(f"Genes Involved:\n")
        for gene in tag_genes:
            if gene["family"] == family:
                f.write(f" {gene['gene_id']} (Start: {gene['start']}, End: {gene['end']})\n")
            else:
                f.write(f" Spacer: {gene['gene_id']}\n")
        f.write("\n")

# Calculate the percentage of tags per chromosome
chromosome_tags = gene_data["chromosome"].value_counts()
tag_counts = pd.Series([tag[0][0]["chromosome"] for tag in tags]).value_counts()
percentage_tags = (tag_counts / chromosome_tags * 100).fillna(0)

# Calculate the number of genes included in tags per chromosome (excluding spacers)
genes_in_tags = {}
for tag_genes, family, spacers in tags:
    chromosome = tag_genes[0]["chromosome"]
    gene_count = len([gene for gene in tag_genes if gene["family"] == family])
    if chromosome in genes_in_tags:
        genes_in_tags[chromosome] += gene_count
    else:
        genes_in_tags[chromosome] = gene_count

# Calculate the number of tags per chromosome
tags_per_chromosome = pd.Series([tag[0][0]["chromosome"] for tag in tags]).value_counts()

# Write all tags to the output file
with open("new MCL/tags_outputLow1.txt", "a") as f: #change path for high/Low data
    f.write("\nAll Tags Information:\n")
    for i, (tag_genes, family, spacers) in enumerate(tags):
        chromosome = tag_genes[0]["chromosome"]
        num_genes = len([gene for gene in tag_genes if gene["family"] == family])
        f.write(f"Tag: {i + 1}\n")
        f.write(f"Chromosome: {chromosome}\n")
        f.write(f"Family: {family}\n")
        f.write(f"Number of Genes: {num_genes}\n")
        f.write(f"Number of Spacers: {spacers}\n")
        f.write(f"Genes Involved:\n")
        for gene in tag_genes:
            if gene["family"] == family:
                f.write(f" {gene['gene_id']} (Start: {gene['start']}, End: {gene['end']})\n")
            else:
                f.write(f" Spacer: {gene['gene_id']}\n")
        f.write("\n")
    # Write the summary to the output file
    f.write("\nSummary of Tags per Chromosome:\n")
    for chromosome, percentage in percentage_tags.items():
        f.write(f"Chromosome: {chromosome}, Percentage of Tags: {percentage:.2f}%\n")
    f.write("\nNumber of Genes in Tags per Chromosome (excluding spacers):\n")
    for chromosome, count in genes_in_tags.items():
        f.write(f"Chromosome: {chromosome}, Number of Genes in Tags: {count}\n")
    f.write("\nNumber of Tags per Chromosome:\n")
    for chromosome, count in tags_per_chromosome.items():
        f.write(f"Chromosome: {chromosome}, Number of Tags: {count}\n")


#VISUALIZE


import os
import matplotlib.pyplot as plt
import pandas as pd

# Ensure the folder exists
output_dir = "new MCL/plots"
os.makedirs(output_dir, exist_ok=True)

# Create a figure with 2 rows and 2 columns
fig, axes = plt.subplots(2, 2, figsize=(15, 12))  # 2x2 grid of subplots

# ---- 1. Number of Tags per Chromosome ----
tags_per_chromosome = pd.Series([tag[0][0]["chromosome"] for tag in tags]).value_counts()
axes[0, 0].bar(tags_per_chromosome.index, tags_per_chromosome.values)
axes[0, 0].set_xlabel('Chromosome')
axes[0, 0].set_ylabel('Number of Tags')
axes[0, 0].set_title('Number of Tags per Chromosome')
axes[0, 0].tick_params(axis='x', rotation=45)

# ---- 2. Number of Genes Inside Tags per Chromosome ----
genes_in_tags_df = pd.DataFrame.from_dict(genes_in_tags, orient='index', columns=['Number of Genes']).reset_index()
genes_in_tags_df.columns = ['Chromosome', 'Number of Genes']
axes[0, 1].bar(genes_in_tags_df['Chromosome'], genes_in_tags_df['Number of Genes'])
axes[0, 1].set_xlabel('Chromosome')
axes[0, 1].set_ylabel('Number of Genes in Tags')
axes[0, 1].set_title('Genes Inside Tags per Chromosome')
axes[0, 1].tick_params(axis='x', rotation=45)

# ---- 3. Percentage of Tags per Chromosome (with labels) ----
percentage_tags_df = percentage_tags.reset_index()
percentage_tags_df.columns = ['Chromosome', 'Percentage of Tags']
bars = axes[1, 0].bar(percentage_tags_df['Chromosome'], percentage_tags_df['Percentage of Tags'])
axes[1, 0].set_xlabel('Chromosome')
axes[1, 0].set_ylabel('Percentage of Tags')
axes[1, 0].set_title('Percentage of Tags per Chromosome')
axes[1, 0].tick_params(axis='x', rotation=45)
# Add percentage labels
for bar in bars:
    height = bar.get_height()
    axes[1, 0].text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}%', 
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

# ---- 4. Largest Tag per Chromosome ----
largest_tag_per_chromosome = {}
for tag_genes, family, spacers in tags:
    chromosome = tag_genes[0]["chromosome"]
    gene_count = len([gene for gene in tag_genes if gene["family"] == family])
    if chromosome not in largest_tag_per_chromosome or gene_count > largest_tag_per_chromosome[chromosome]:
        largest_tag_per_chromosome[chromosome] = gene_count

# Plot the largest tag per chromosome
axes[1, 1].bar(largest_tag_per_chromosome.keys(), largest_tag_per_chromosome.values(), color='orange')
axes[1, 1].set_xlabel('Chromosome')
axes[1, 1].set_ylabel('Number of Genes in Largest Tag')
axes[1, 1].set_title('Largest Tag per Chromosome')
axes[1, 1].tick_params(axis='x', rotation=45)

# Add the number of genes on top of each bar
for chromosome, gene_count in largest_tag_per_chromosome.items():
    axes[1, 1].text(chromosome, gene_count + 0.1, str(gene_count), ha='center', va='bottom', fontsize=10)

# Adjust layout for clarity
plt.tight_layout()

# Save the combined figure
plt.savefig(f"{output_dir}/combined_plot_low.png") #change name for high / low stringent data

# Show the combined plot
plt.show()
