import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. DATABASE SETUP (PYTHON TO SQL)
# ==========================================
print("Initializing SQL Database Engine...")
file_path = "Dataset for Data Analytics.xlsx"
df = pd.read_excel(r"D:\Decode Labs\Project 02\Dataset for Data Analytics.xlsx")

# Create an in-memory SQLite database
conn = sqlite3.connect(':memory:')

# Push the Pandas DataFrame into a SQL table named 'transactions'
df.to_sql('transactions', conn, index=False)

# ==========================================
# 2. SQL QUERY 1: THE WHERE FUNNEL
# ==========================================
# Goal: Isolate specific categories using WHERE before aggregating
print("\n--- QUERY 1: Revenue for High-Volume Orders ---")
query_1 = """
SELECT 
    Product,
    COUNT(*) AS Total_Transactions,
    SUM(TotalPrice) AS Total_Revenue,
    AVG(TotalPrice) AS Avg_Order_Value
FROM transactions
WHERE ItemsInCart >= 5
GROUP BY Product
ORDER BY Total_Revenue DESC;
"""
df_q1 = pd.read_sql_query(query_1, conn)
print(df_q1.to_string())

# ==========================================
# 3. SQL QUERY 2: EXECUTION ORDER MASTERY (HAVING)
# ==========================================
# Goal: Use GROUP BY and HAVING to filter aggregated buckets
print("\n--- QUERY 2: Identifying VIP Customers (Spend > $3000) ---")
query_2 = """
SELECT 
    CustomerID,
    COUNT(OrderID) AS Purchase_Count,
    SUM(TotalPrice) AS Lifetime_Value
FROM transactions
GROUP BY CustomerID
HAVING SUM(TotalPrice) > 3000
ORDER BY Lifetime_Value DESC
LIMIT 5;
"""
df_q2 = pd.read_sql_query(query_2, conn)
print(df_q2.to_string())

# ==========================================
# 4. SQL QUERY 3: CATEGORICAL AGGREGATION
# ==========================================
print("\n--- QUERY 3: Payment Method Performance ---")
query_3 = """
SELECT 
    PaymentMethod,
    SUM(TotalPrice) AS Total_Revenue,
    COUNT(OrderID) AS Transaction_Volume
FROM transactions
WHERE OrderStatus = 'Shipped' OR OrderStatus = 'Delivered'
GROUP BY PaymentMethod
ORDER BY Total_Revenue DESC;
"""
df_q3 = pd.read_sql_query(query_3, conn)
print(df_q3.to_string())

# ==========================================
# 5. VISUALIZING THE SQL OUTPUT
# ==========================================
print("\nGenerating SQL Insights Dashboard...")
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('SQL Extraction Insights', fontsize=16, fontweight='bold')

# Chart 1: Revenue from Query 1
sns.barplot(data=df_q1, x='Total_Revenue', y='Product', palette='viridis', ax=axes[0], hue='Product', legend=False)
axes[0].set_title('Revenue from High-Volume Carts (Items >= 5)')
axes[0].set_xlabel('Total Revenue ($)')
axes[0].set_ylabel('')

# Chart 2: Payment Methods from Query 3
sns.barplot(data=df_q3, x='PaymentMethod', y='Total_Revenue', palette='magma', ax=axes[1], hue='PaymentMethod', legend=False)
axes[1].set_title('Successful Revenue by Payment Method')
axes[1].set_ylabel('Total Revenue ($)')
axes[1].set_xlabel('Payment Method')

plt.tight_layout()
plt.savefig('SQL_Insights_Project3.jpg', dpi=300)
print("Success: 'SQL_Insights_Project3.jpg' saved to workspace.")

# Close the database connection
conn.close()