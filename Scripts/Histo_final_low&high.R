# Load necessary libraries
library(ggplot2)
library(dplyr)

# Define the file path (update this with your actual file path)
#mcl_file <- "highstringentMCL.tabular"

# Read the MCL file (assuming tab-delimited format)
#mcl_data <- read.delim(mcl_file, header = FALSE, stringsAsFactors = FALSE)

# Compute cluster sizes
cluster_sizes <- rowSums(lowstringentMCL != "")  #change for lowstringentMCL #Count non-empty columns per row

# Find the largest cluster
max_size <- max(cluster_sizes)
largest_cluster_index <- which(cluster_sizes == max_size)

# Create a data frame for plotting
df <- data.frame(ClusterSize = cluster_sizes)

# Plot histogram with the largest cluster highlighted
ggplot(df, aes(x = ClusterSize)) +
  geom_histogram(binwidth = 5, fill = "pink", color = "black", alpha = 0.7) +
  geom_vline(aes(xintercept = max_size), color = "red", linetype = "dashed", size = 1) +
  geom_text(aes(x = max_size, y = 10, label = paste("Largest Cluster:", max_size)), 
            color = "red", vjust = -0.5, size = 5) +
  theme_minimal() +
  labs(title = "Distribution of Low Stringent Cluster Sizes",
       x = "Cluster size (Number of genes per family)",
       y = "Frequency") +
  theme(plot.title = element_text(hjust = 0.5, size = 14, face = "bold"))

# Add a density plot overlay
ggplot(df, aes(x = ClusterSize)) +
  geom_density(fill = "blue", alpha = 0.4) +
  geom_vline(aes(xintercept = max_size), color = "red", linetype = "dashed", size = 1) +
  geom_text(aes(x = max_size, y = 0.02, label = paste("Largest Cluster:", max_size)), 
            color = "red", vjust = -0.5, size = 5) +
  theme_minimal() +
  labs(title = "Density Plot of Low Stringent Cluster Sizes",
       x = "Cluster Size",
       y = "Density") +
  theme(plot.title = element_text(hjust = 0.5, size = 14, face = "bold"))

##to count the singletons
# Count the number of genes per family
cluster_sizes <- apply(highstringentMCL  , 1, function(x) sum(x != ""))  # Count non-empty entries in each row

# Identify singletons (clusters of size 1)
singletons_count <- sum(cluster_sizes == 1)

# Print result
cat("Number of singletons:", singletons_count, "\n")
