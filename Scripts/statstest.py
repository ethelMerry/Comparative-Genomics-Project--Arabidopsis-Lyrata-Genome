import pandas as pd
from scipy.stats import shapiro, mannwhitneyu, ttest_ind, levene, ks_2samp

# Load the data from the CSV file
data = pd.read_csv("KAKS/annotated_ks1.csv")

# Separate the data into Tag and Non-Tag groups
tag_data = data[data['Tag_Status'] == 'Tag']['Ks']
non_tag_data = data[data['Tag_Status'] == 'Non-Tag']['Ks']

# Initialize summary
summary = {}

# --- Kolmogorov-Smirnov Test ---
ks_stat, ks_p_value = ks_2samp(tag_data, non_tag_data)
summary['Kolmogorov-Smirnov Test'] = {
    'statistic': ks_stat,
    'p_value': ks_p_value
}

# --- Shapiro-Wilk Test for normality ---
stat_tag, p_tag = shapiro(tag_data)
stat_non_tag, p_non_tag = shapiro(non_tag_data)

summary['Shapiro-Wilk Test (Tag)'] = {
    'statistic': stat_tag,
    'p_value': p_tag
}
summary['Shapiro-Wilk Test (Non-Tag)'] = {
    'statistic': stat_non_tag,
    'p_value': p_non_tag
}

# --- Mann-Whitney U Test (Non-Parametric) ---
mann_whitney_stat, mann_whitney_p_value = mannwhitneyu(tag_data, non_tag_data, alternative='two-sided')
summary['Mann-Whitney U Test'] = {
    'statistic': mann_whitney_stat,
    'p_value': mann_whitney_p_value
}

# --- Levene's Test for Equality of Variance ---
levene_stat, levene_p_value = levene(tag_data, non_tag_data)
summary['Levene\'s Test'] = {
    'statistic': levene_stat,
    'p_value': levene_p_value
}

# --- Independent t-test (If Levene's test is not significant) ---
if levene_p_value >= 0.05:
    t_stat, t_p_value = ttest_ind(tag_data, non_tag_data)
    summary['Independent t-test'] = {
        'statistic': t_stat,
        'p_value': t_p_value
    }
else:
    summary['Independent t-test'] = {
        'statistic': None,
        'p_value': "Not applicable due to unequal variances"
    }

# Print Summary of Results
print("\nStatistical Test Results:")
for test, result in summary.items():
    print(f"\n{test}:")
    for key, value in result.items():
        print(f"  {key}: {value}")

# Determine significance based on p-value < 0.05
print("\nSummary of Significance:")
for test, result in summary.items():
    if 'p_value' in result:
        if isinstance(result['p_value'], float) and result['p_value'] < 0.05:
            print(f"{test} indicates a significant result (p-value < 0.05).")
        else:
            print(f"{test} does not indicate a significant result (p-value >= 0.05).")
