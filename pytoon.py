
#Import Libraries


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Load Dataset
df = pd.read_csv("Tadawul_stcks.csv")

#Data Exploration


print(df.head())

print(df.shape)

print(df.info())

print(df.describe())

print(df.isnull().sum())

# Data Cleaning

# Remove spaces from column names
df.columns = df.columns.str.strip()

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Remove duplicate rows
df = df.drop_duplicates()

# Fill missing numeric values with median
numeric_cols = df.select_dtypes(include=np.number).columns

for col in numeric_cols:
    df[col] = df[col].fillna(df[col].median())

# Fill missing text values with "Unknown"
object_cols = df.select_dtypes(include="object").columns

for col in object_cols:
    df[col] = df[col].fillna("Unknown")

# Save cleaned dataset
df.to_csv("clean_data.csv", index=False)

# Exploratory Data Analysis

# 1. Distribution of Close Price
plt.figure(figsize=(8,5))
plt.hist(df["close"], bins=30)
plt.title("Distribution of Close Price")
plt.xlabel("Close Price")
plt.ylabel("Frequency")
plt.show()

# 2. Sector Count
plt.figure(figsize=(12,6))
sns.countplot(data=df, y="sectoer", order=df["sectoer"].value_counts().index)
plt.title("Number of Companies in Each Sector")
plt.show()

# 3. Boxplot of Close Price
plt.figure(figsize=(8,5))
sns.boxplot(x=df["close"])
plt.title("Boxplot of Close Price")
plt.show()

# 4. Open vs Close
plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x="open", y="close")
plt.title("Open vs Close Price")
plt.show()

# 5. groupb to get  Average Close Price by Sector
sector_avg = df.groupby("sectoer")["close"].mean().sort_values()

plt.figure(figsize=(12,6))
sector_avg.plot(kind="bar")
plt.title("Average Close Price by Sector")
plt.ylabel("Average Close")
plt.show()

# 6. Correlation Heatmap
plt.figure(figsize=(10,8))

corr = df.select_dtypes(include=np.number).corr()

sns.heatmap(corr, annot=True, cmap="Blues")

plt.title("Correlation Heatmap")
plt.show()


# Insights


print("-- KEY INSIGHTS -")

# Total number of companies
if "symbol" in df.columns:
    print("Total Companies:", df["symbol"].nunique())

# Average Close Price
if "close" in df.columns:
    print("Average Close Price:", round(df["close"].mean(), 2))
    print("Highest Close Price:", df["close"].max())
    print("Lowest Close Price:", df["close"].min())

# Highest Average Close Price by Sector
if "sectoer" in df.columns and "close" in df.columns:

    sector_avg = df.groupby("sectoer")["close"].mean()

    print("\nSector with Highest Average Close Price:")
    print(sector_avg.idxmax())

    print("\nSector with Lowest Average Close Price:")
    print(sector_avg.idxmin())

# Highest Opening Price
if "open" in df.columns:
    highest_open = df.loc[df["open"].idxmax()]

    print("\nCompany with Highest Opening Price:")

    if "symbol" in df.columns:
        print(highest_open["symbol"])

    print("Opening Price:", highest_open["open"])

# Highest Closing Price
if "close" in df.columns:
    highest_close = df.loc[df["close"].idxmax()]

    print("\nCompany with Highest Closing Price:")

    if "symbol" in df.columns:
        print(highest_close["symbol"])

    print("Closing Price:", highest_close["close"])

# Missing Values
print("\nTotal Missing Values:")
print(df.isnull().sum().sum())
