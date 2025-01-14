# -*- coding: utf-8 -*-
"""Week14_LiveCodingSession_Tasks.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SPZnScUQy0JEShSC7PukfCMZFXIMQVwN
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import time

import random
from sklearn.model_selection import train_test_split

import sys
sys.path.append("..")

#For content based recommendation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import re
# %matplotlib inline
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('https://storage.googleapis.com/ty2020/reco.csv.gz')

df = df[df.index < 55000]

df.head()

"""**TASK-14A:** Please find the 5 most frequent ones for the following columns:

user_id
productcontent_id
brand_id
category_id
color_id
"""

# user_id 
import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(20,10))
sns.countplot(x='user_id', data=df, palette='gist_earth',
             order=df['user_id'].value_counts()[:5]\
             .sort_values().index).set_title("Top 5 User", fontsize=15,
                                             weight='bold')

# productcontentid 
import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(20,10))
sns.countplot(x='productcontentid', data=df, palette='gist_earth',
             order=df['productcontentid'].value_counts()[:5]\
             .sort_values().index).set_title("Top 5 Product", fontsize=15,
                                             weight='bold')

# brand _id
plt.figure(figsize=(20,10))
sns.countplot(x='brand_id', data=df, palette='gist_earth',
             order=df['brand_id'].value_counts()[:5]\
             .sort_values().index).set_title("Top 5 Brand", fontsize=15,
                                             weight='bold')

# category_id
plt.figure(figsize=(20,10))
sns.countplot(x='category_id', data=df, palette='gist_earth',
             order=df['category_id'].value_counts()[:5]\
             .sort_values().index).set_title("Top 5 Category", fontsize=15,
                                             weight='bold')

# color_id
plt.figure(figsize=(20,10))
sns.countplot(x='color_id', data=df, palette='gist_earth',
             order=df['color_id'].value_counts().iloc[:5].sort_values().index).set_title("Top 5 Color", fontsize=15,
                                             weight='bold')

"""**TASK-14B:** Please provide histograms for the relevant columns and provide your comments very briefly."""

# user_id
plt.figure(figsize=(20,10))
sns.histplot(data=df, x="user_id", kde=True)
plt.xlabel("User Id")
plt.title("User Id Distribution")
# Although there are prominent columns, a growing distribution is seen in general. 
# Considering that users get their id numbers in order, we can assume that older people get the first numbers. 
# The higher rate of new generation people using and adapting to technology may have affected the distribution.

# productcontentid
plt.figure(figsize=(20,10))
sns.histplot(data=df, x="productcontentid", kde=True)
plt.xlabel("Product Id")
plt.title(" Product Content Id Distribution")
# It is difficult to see the distribution as there are serious differences between the number of products purchased. 
# I will use log transformation method in next cell to avoid this situation

# productcontentid log10
plt.figure(figsize=(20,10))
sns.histplot(data=df, x="productcontentid", kde=True, log_scale=10)
plt.xlabel("Product Content Id (log$_{10}$) ")
plt.title("Product Content Id Distribution")
# Despite the applied transformation method, an uneven distribution is observed. 
# Considering that the ids given to the products added by the sellers are given increasing numerical values in order, I think that a noticeable increase is observed in the distribution of the products because the recently added products are in line with the customer demands

# brand_id
plt.figure(figsize=(20,10))
sns.histplot(data=df, x="brand_id", kde=True)
plt.xlabel("Brand Id")
plt.title("Brand Id Distribution")
# It is difficult to see the distribution as there are serious differences between the number of brands. 
# I will use log transformation method in next cell to avoid this situation

# brand_id log10
plt.figure(figsize=(20,10))
sns.histplot(data=df, x="brand_id", kde=True, log_scale=10)
plt.xlabel("Brand Id (log$_{10}$) ")
plt.title("Brand Id Distribution")
# Although there are brands that cause noticeable deterioration at the beginning and at the end, we can say that there is a similar to normal distrubution.

# category_id 
plt.figure(figsize=(20,10))
sns.histplot(data=df, x="category_id", kde=True)
plt.xlabel("Category Id")
plt.title("Category Id Distribution")
# Observed  like a uniformdistribution even though there are outlier columns 
# Outlier columns may consist of these products, as consumables require repurchasing.

# color_id
plt.figure(figsize=(20,10))
sns.histplot(data=df, x="color_id", kde=True)
plt.xlabel("Color Id")
plt.title("Category Id Distribution")
# It is difficult to see the distribution as there are serious differences between the number of color. 
# I will use log transformation method in next cell to avoid this situation

# color_id log10
plt.figure(figsize=(20,10))
sns.histplot(data=df, x="color_id", kde=True, log_scale=10)
plt.xlabel("Color Id (log$_{10}$) ")
plt.title("Color Id Distribution")
# We observe that the colors in the first half of the graph are used more. Because giving the first id numbers for the main and familiar colors and using new id numbers for the fancy colors can cause the graphic to be formed in this way.

"""**TASK-14C:** Please provide pivot table for illustrating the distribution of product genders with respect to the business units."""

product_gender_dist = df.pivot_table(index="gender",columns="business_unit",values="user_id",aggfunc='count')
product_gender_dist

"""**TASK-14D:** Please provide the price histogram for the most frequent 3 category names separately."""

# Find top three product category name 
top_3_prod_categories = df.groupby('category_name')['price'].count().sort_values(ascending=False).head(3)
top_3_prod_categories

# Creates a new dataframe that include only top three category and other features from old df
top_3_product_df = pd.DataFrame()
for i in top_3_prod_categories.index:
   top_3_product_df = top_3_product_df.append(df[df["category_name"]==i])
top_3_product_df

top_3_product_df.category_name.unique() # Checks the new dataframe whether include only top 3 product category

import matplotlib.pyplot as plt
import seaborn as sns
# Visualazation of the price histogram for the most frequent 3 category names separately. (log 10 transformation)
plt.figure(figsize=(20,10))
sns.histplot(x='price', data=top_3_product_df, palette='gist_earth',hue="category_name", log_scale=10)
plt.title("Price Distrubutions of Top 3 Product (log10) ", fontsize=15,
                                             weight='bold')

# Visualazation of the price histogram for the most frequent 3 category names separately. (log 10 transformation)
sns.displot(
  data=top_3_product_df,
  x="price",
  col="category_name",
  kind="hist",
  aspect=1.4,
  log_scale=10,
  bins=10
)

# Visualazation of the price histogram for the most frequent 3 category names separately.
sns.displot(
  data=top_3_product_df,
  x="price",
  col="category_name",
  kind="hist",
  aspect=1.4,
  bins=10
)

# Visualazation of the price histogram for the most frequent 3 category names separately.
plt.figure(figsize=(20,10))
sns.histplot(x='price', data=top_3_product_df, palette='gist_earth',hue="category_name")
plt.title("Price Distrubutions of Top 3 Product ", fontsize=15,
                                             weight='bold')

"""**TASK-14E:** Please find the customer who has spent the highest amount of money."""

highest_spend = df.groupby("user_id")["price"].sum().sort_values(ascending=False)
highest_spend[0:1]

"""**TASK-14F:** Please find the customer(s) who has the most various brands, then categories and then business units."""

# Customer(s) who has the most various  brands
most_varios_brands = df.pivot_table(index="user_id",columns="brand_id",values="ImageLink",aggfunc="count") # Creates pivot table that include all brand and all user.
most_varios_brands.fillna(value=0,inplace=True) # Fill null values with 0
most_varios_brands[most_varios_brands>0]=1 # If the values is bigger than 0 that changes this value with 1 for summation all unique brands.
most_varios_brands.sum(axis=1).sort_values(ascending=False)[0:1] # Sums all rows then sorts the sum values in ascending order then gets first one.

# Customer(s) who has the most various categories
most_varios_categories = df.pivot_table(index="user_id",columns="category_id",values="ImageLink",aggfunc="count") # Creates pivot table that include all category and all user.
most_varios_categories.fillna(value=0,inplace=True) # Fill null values with 0
most_varios_categories[most_varios_categories>0]=1 # If the values is bigger than 0 that changes this value with 1 for summation all unique category.
most_varios_categories.sum(axis=1).sort_values(ascending=False)[0:1] # Sums all rows then sorts the sum values in ascending order then gets first one.

# Customer(s) who has the most various business units.
most_varios_business_unit = df.pivot_table(index="user_id",columns="business_unit",values="ImageLink",aggfunc="count") # Creates pivot table that include all business_unit and all user.
most_varios_business_unit.fillna(value=0,inplace=True) # Fill null values with 0
most_varios_business_unit[most_varios_business_unit>0]=1 # If the values is bigger than 0 that changes this value with 1 for summation all unique business_unit.
most_varios_business_unit.sum(axis=1).sort_values(ascending=False)[0:1] # Sums all rows then sorts the sum values in ascending order then gets first one.

"""**TASK-14G:** Please find the product that is sold at the highest level between 12.08.2020 and 15.08.2020"""

df['partition_date'] = pd.to_datetime(df['partition_date']) # Changes object to datetime object

df[(df["partition_date"]<"2020-08-15")&(df["partition_date"]>"2020-08-12")]["price"].max() # Gets the highest level between 12.08.2020 and 15.08.2020

"""**TASK-14H:** Please find the unisex product that has the highest price."""

df[df["gender"]=="Unisex"]["price"].max()

"""**TASK-14I:** Please determine the product id that brought the highest amount of money/cash."""

df.groupby("productcontentid")["price"].sum().sort_values(ascending=False)[:1]

"""**TASK-14J:** Please the number of different products that is for female and has the color codes 8, 11, or 9."""

df[(df["gender"]=="Kadın")&((df["color_id"]==8) | (df["color_id"]==11) | (df["color_id"]==9))].groupby("productcontentid")["productcontentid"].count()