import pandas as pd
import numpy as np
from scipy.stats import shapiro, mannwhitneyu, levene, fligner

# Dataset 1: Elovl
# Control: 8 sequences, 9 CpG sites
data1_control = np.zeros((8, 9), dtype=int)
data1_control[0:2, 0:3] = 1  # 2 sequences with 3 methylated sites
# Remaining 6 sequences have 0 methylated sites (already set to 0)
df1_control = pd.DataFrame(data1_control, columns=[f'CpG_{i+1}' for i in range(9)])
df1_control['Methylation_Percentage'] = df1_control.mean(axis=1) * 100

# Perturbation: 10 sequences, 9 CpG sites
data1_perturbation = np.zeros((10, 9), dtype=int)
data1_perturbation[0, 0:1] = 1  # 1 sequence with 1 methylated site
data1_perturbation[1, 0:2] = 1  # 1 sequence with 2 methylated sites
data1_perturbation[2, 0:3] = 1  # 1 sequence with 3 methylated sites
data1_perturbation[3, 0:4] = 1  # 1 sequence with 4 methylated sites
# Remaining 5 sequences have 0 methylated sites (already set to 0)
df1_perturbation = pd.DataFrame(data1_perturbation, columns=[f'CpG_{i+1}' for i in range(9)])
df1_perturbation['Methylation_Percentage'] = df1_perturbation.mean(axis=1) * 100

# Dataset 2: Collagen
# Control: 9 sequences, 11 CpG sites
data2_control = np.zeros((9, 11), dtype=int)
for i in range(9):
    data2_control[i, 0] = 1  # Every sequence has at least 1 methylated site
for i in range(4):
    data2_control[i, 1] = 1  # First 4 sequences have 2 methylated sites
df2_control = pd.DataFrame(data2_control, columns=[f'CpG_{i+1}' for i in range(11)])
df2_control['Methylation_Percentage'] = df2_control.mean(axis=1) * 100

# Perturbation: 5 sequences, 11 CpG sites
data2_perturbation = np.zeros((5, 11), dtype=int)
data2_perturbation[0, :5] = 1  # 1 sequence with 5 methylated sites
data2_perturbation[1:4, :4] = 1  # 3 sequences with 4 methylated sites
data2_perturbation[4, :3] = 1  # 1 sequence with 3 methylated sites
df2_perturbation = pd.DataFrame(data2_perturbation, columns=[f'CpG_{i+1}' for i in range(11)])
df2_perturbation['Methylation_Percentage'] = df2_perturbation.mean(axis=1) * 100

# Function to perform statistical tests
def perform_statistical_tests(control, perturbation, dataset_name):
    print(f"\n=== {dataset_name} ===")
    
    # Step 1: Test for normality (Shapiro-Wilk test)
    print("Normality Test (Shapiro-Wilk):")
    stat, p_control = shapiro(control)
    print(f"Control: p-value = {p_control:.4f}")
    stat, p_perturbation = shapiro(perturbation)
    print(f"Perturbation: p-value = {p_perturbation:.4f}")

    # Step 2: Test for difference in means (Mann-Whitney U test)
    print("\nTest for Difference in Means (Mann-Whitney U test):")
    stat, p_mean = mannwhitneyu(control, perturbation, alternative='two-sided')
    print(f"p-value = {p_mean:.4f}")

    # Step 3: Test for difference in variances (Levene's test and Fligner-Killeen test)
    print("\nVariance Test (Levene's Test):")
    stat, p_levene = levene(control, perturbation, center='median')
    print(f"p-value = {p_levene:.4f}")

    print("\nVariance Test (Fligner-Killeen Test):")
    stat, p_fligner = fligner(control, perturbation)
    print(f"p-value = {p_fligner:.4f}")

    # Step 4: Compare means and standard deviations
    print(f"\nSummary Statistics:")
    print(f"Control Mean: {np.mean(control):.2f}%, SD: {np.std(control, ddof=1):.2f}%")
    print(f"Perturbation Mean: {np.mean(perturbation):.2f}%, SD: {np.std(perturbation, ddof=1):.2f}%")

# Perform tests for both datasets
perform_statistical_tests(df1_control['Methylation_Percentage'], df1_perturbation['Methylation_Percentage'], "Dataset 1")
perform_statistical_tests(df2_control['Methylation_Percentage'], df2_perturbation['Methylation_Percentage'], "Dataset 2 (Collagen)")