import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patheffects as path_effects

# Define the first dataset (Control: 9 sequences, 11 CpG sites)
data1 = np.zeros((9, 11), dtype=int)  # Initially all unmethylated
for i in range(9):
    data1[i, 0] = 1  # Every sequence has at least one methylated site
for i in range(4):
    data1[i, i + 1] = 1  # Incrementally add one more methylation site to first four sequences
df1 = pd.DataFrame(data1, columns=[f'CpG_{i+1}' for i in range(11)])
df1['Methylation_Percentage'] = df1.mean(axis=1) * 100

# Define the second dataset (CSE: 5 sequences, 11 CpG sites)
data2 = np.zeros((5, 11), dtype=int)  # Initially all unmethylated
data2[0, :5] = 1  # First sequence: 5 methylated sites
data2[1:4, :4] = 1  # Next three sequences: 4 methylated sites
data2[4, :3] = 1  # Last sequence: 3 methylated sites
df2 = pd.DataFrame(data2, columns=[f'CpG_{i+1}' for i in range(11)])
df2['Methylation_Percentage'] = df2.mean(axis=1) * 100

# Create the boxplots side by side in grayscale
plt.figure(figsize=(12, 6), dpi = 300)
sns.set_palette("gray")

min_y = 0  # Ensure y-axis starts at 0
max_y = max(df1['Methylation_Percentage'].max(), df2['Methylation_Percentage'].max()) + 5  # Extend upper limit

plt.subplot(1, 2, 1)
sns.boxplot(y=df1['Methylation_Percentage'], color='gray', width=0.5)
sns.stripplot(y=df1['Methylation_Percentage'], color='black', jitter=True, alpha=0.7)
mean1 = df1['Methylation_Percentage'].mean()
plt.axhline(y=mean1, color='black', linestyle='--', label='Mean', linewidth = 3)
plt.text(0.02, mean1 + 1.5, f'{mean1:.1f}%', color='black', fontsize=22, fontweight='bold',
         path_effects=[path_effects.withStroke(linewidth=2, foreground='black')])
plt.tick_params(width = 2)
plt.tick_params(axis='y', which='major', labelsize=14)
plt.ylabel('Methylation Percentage', fontsize = 14)
plt.ylim(min_y, max_y)
plt.title('Control', fontsize = 16)
plt.legend(fontsize=16)

plt.subplot(1, 2, 2)
sns.boxplot(y=df2['Methylation_Percentage'], color='gray', width=0.5)
sns.stripplot(y=df2['Methylation_Percentage'], color='black', jitter=True, alpha=0.7)
mean2 = df2['Methylation_Percentage'].mean()
plt.axhline(y=mean2, color='black', linestyle='--', label='Mean', linewidth = 3)
plt.text(0.02, mean2 + 1.5, f'{mean2:.1f}%', color='black', fontsize=22, fontweight='bold',
         path_effects=[path_effects.withStroke(linewidth=2, foreground='black')])
plt.tick_params(width = 2)
plt.tick_params(axis='y', which='major', labelsize=14)
plt.ylabel('Methylation Percentage', fontsize = 14)
plt.ylim(min_y, max_y)
plt.title('CSE', fontsize = 16)
plt.legend(fontsize=16)

plt.suptitle('COL1 Methylation Percentages', fontsize=14, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('Col1-Methylation.png', dpi = 300)
