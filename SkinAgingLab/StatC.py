import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu, levene, fligner

# Dataset 1: Elovl
# Control: 8 sequences, 9 CpG sites
data1_control = np.zeros((8, 9), dtype=int)
data1_control[0:2, 0:3] = 1  # 2 sequences with 3 methylated sites
df1_control = pd.DataFrame(data1_control, columns=[f'CpG_{i+1}' for i in range(9)])

# Perturbation: 10 sequences, 9 CpG sites
data1_perturbation = np.zeros((10, 9), dtype=int)
data1_perturbation[0, 0:1] = 1  # 1 sequence with 1 methylated site
data1_perturbation[1, 0:2] = 1  # 1 sequence with 2 methylated sites
data1_perturbation[2, 0:3] = 1  # 1 sequence with 3 methylated sites
data1_perturbation[3, 0:4] = 1  # 1 sequence with 4 methylated sites
df1_perturbation = pd.DataFrame(data1_perturbation, columns=[f'CpG_{i+1}' for i in range(9)])

# Dataset 2: Collagen
# Control: 9 sequences, 11 CpG sites
data2_control = np.zeros((9, 11), dtype=int)
for i in range(9):
    data2_control[i, 0] = 1  # Every sequence has at least 1 methylated site
for i in range(4):
    data2_control[i, 1] = 1  # First 4 sequences have 2 methylated sites
df2_control = pd.DataFrame(data2_control, columns=[f'CpG_{i+1}' for i in range(11)])

# Perturbation: 5 sequences, 11 CpG sites
data2_perturbation = np.zeros((5, 11), dtype=int)
data2_perturbation[0, :5] = 1  # 1 sequence with 5 methylated sites
data2_perturbation[1:4, :4] = 1  # 3 sequences with 4 methylated sites
data2_perturbation[4, :3] = 1  # 1 sequence with 3 methylated sites
df2_perturbation = pd.DataFrame(data2_perturbation, columns=[f'CpG_{i+1}' for i in range(11)])

# Function to perform statistical tests across columns
def perform_statistical_tests(control, perturbation, dataset_name):
    print(f"\n=== {dataset_name} ===")
    
    # Step 1: Calculate methylation percentage for each CpG site (column)
    control_percentages = control.sum(axis=0) / control.shape[0] * 100
    perturbation_percentages = perturbation.sum(axis=0) / perturbation.shape[0] * 100

    # Step 2: Calculate mean and standard deviation of percentages
    control_mean = np.mean(control_percentages)
    perturbation_mean = np.mean(perturbation_percentages)
    control_std = np.std(control_percentages, ddof=1)  # Standard deviation (ddof=1 for sample std)
    perturbation_std = np.std(perturbation_percentages, ddof=1)  # Standard deviation (ddof=1 for sample std)

    # Step 3: Test for difference in mean methylation percentages (Mann-Whitney U test)
    stat, p_mean = mannwhitneyu(control_percentages, perturbation_percentages, alternative='two-sided')
    print(f"Mean Comparison (Mann-Whitney U test): p-value = {p_mean:.4f}")

    # Step 4: Test for difference in variances (Levene's test and Fligner-Killeen test)
    stat, p_levene = levene(control_percentages, perturbation_percentages, center='median')
    print(f"Variance Comparison (Levene's Test): p-value = {p_levene:.4f}")

    stat, p_fligner = fligner(control_percentages, perturbation_percentages)
    print(f"Variance Comparison (Fligner-Killeen Test): p-value = {p_fligner:.4f}")

    # Step 5: Display the calculated means and standard deviations
    print(f"\nSummary Statistics:")
    print(f"Control Mean Percentage: {control_mean:.2f}%")
    print(f"Perturbation Mean Percentage: {perturbation_mean:.2f}%")
    print(f"Control Standard Deviation of Percentages: {control_std:.2f}")
    print(f"Perturbation Standard Deviation of Percentages: {perturbation_std:.2f}")

# Perform tests for both datasets
perform_statistical_tests(df1_control, df1_perturbation, "Dataset 1 (Elovl)")
perform_statistical_tests(df2_control, df2_perturbation, "Dataset 2 (Collagen)")
