import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set a clean, "Clinical White" style as recommended in the visual guidelines
sns.set_theme(style="whitegrid")

# ==========================================
# 1. LOAD THE RAW EVIDENCE
# ==========================================
file_path = "Dataset for Data Analytics.xlsx"
df = pd.read_excel(r"D:\Decode Labs\Project 02\Dataset for Data Analytics.xlsx")

# ==========================================
# 2. THE FIVE-NUMBER SUMMARY & CENTER OF GRAVITY
# ==========================================
print("--- THE FIVE-NUMBER SUMMARY ---")
summary_stats = df[['Quantity', 'UnitPrice', 'ItemsInCart', 'TotalPrice']].describe()
print(summary_stats)

mean_tp = df['TotalPrice'].mean()
median_tp = df['TotalPrice'].median()

print("\n--- CENTER OF GRAVITY: MEAN VS MEDIAN ---")
print(f"Total Price - Mean (Sensitive to outliers): ${mean_tp:.2f}")
print(f"Total Price - Median (Robust to anomalies): ${median_tp:.2f}")

if mean_tp > median_tp:
    print("Diagnosis: The Mean is higher than the Median. The distribution is RIGHT-SKEWED (pulled by high-value outlier transactions).")

# ==========================================
# 3. CORRELATION ANALYSIS (MAPPING RELATIONSHIPS)
# ==========================================
print("\n--- CORRELATION ANALYSIS (Pearson r) ---")
numeric_cols = df.select_dtypes(include=[np.number])
correlation_matrix = numeric_cols.corr()
print("Correlation strength with TotalPrice:")
print(correlation_matrix['TotalPrice'].sort_values(ascending=False))

# ==========================================
# 4. VISUAL EVIDENCE (THE DASHBOARD)
# ==========================================
print("\nGenerating Visual Evidence Dashboard...")

# Create a 2x2 grid for our stakeholder visuals
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle('Diagnostic Framework: Exploratory Data Analysis (EDA)', fontsize=18, fontweight='bold')

# A. Univariate: Histogram (The Shape of the Evidence)
sns.histplot(df['TotalPrice'], bins=40, kde=True, color='teal', ax=axes[0, 0])
axes[0, 0].set_title('Distribution of Total Price (Center of Gravity)', fontsize=14)
axes[0, 0].set_xlabel('Total Price ($)')
axes[0, 0].axvline(mean_tp, color='red', linestyle='--', label=f'Mean: ${mean_tp:.0f}')
axes[0, 0].axvline(median_tp, color='blue', linestyle='-', label=f'Median: ${median_tp:.0f}')
axes[0, 0].legend()

# B. Univariate: Boxplot (The Fingerprint of Variability)
sns.boxplot(x=df['TotalPrice'], color='lightblue', ax=axes[0, 1])
axes[0, 1].set_title('Boxplot of Total Price (Locating the Suspects)', fontsize=14)
axes[0, 1].set_xlabel('Total Price ($)')

# C. Bivariate: Scatter Plot (Mapping Relationships)
sns.scatterplot(data=df, x='ItemsInCart', y='TotalPrice', alpha=0.6, color='purple', ax=axes[1, 0])
axes[1, 0].set_title('Correlation: Items In Cart vs Total Price', fontsize=14)
axes[1, 0].set_xlabel('Items In Cart')
axes[1, 0].set_ylabel('Total Price ($)')

# D. Categorical Insight: Revenue by Product (No 3D Effects, pure signal)
product_sales = df.groupby('Product')['TotalPrice'].sum().sort_values(ascending=False)
sns.barplot(x=product_sales.values, y=product_sales.index, palette='mako', ax=axes[1, 1])
axes[1, 1].set_title('Total Revenue by Product', fontsize=14)
axes[1, 1].set_xlabel('Total Revenue ($)')
axes[1, 1].set_ylabel('')

# Clean up layout and save the verified insight
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('EDA_Dashboard_Project2.png', dpi=300)
print("Success: 'EDA_Dashboard_Project2.png' has been saved to your workspace!")

# Display the dashboard on screen
plt.show()