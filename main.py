import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data.csv") # Load the dataset

# data cleaning & preparation
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

# numerical column cleaning
df["price"] = df["price"].astype(str).str.replace('$', '').str.replace(',', '').astype(int)
df["rate_per_sqft"] = df["rate_per_sqft"].astype(str).str.replace('$', '').str.replace(',', '').astype(int)

# categorical columns cleaning
df["status"] = df['status'].str.strip().str.lower()
df["rera_approval"] = df['rera_approval'].str.strip().str.lower().map({"approved by rera": True, "not approved by rera": False})
df["flat_type"] = df['flat_type'].str.strip().str.lower()
df = df.drop_duplicates()  


# Question1- which is the costliest flat?
costliest_flat = df.loc[df['price'].idxmax()]

print(f"The costliest flat in the dataset is a {costliest_flat['bhk_count']} BHK {costliest_flat['flat_type']} located in {costliest_flat['locality']} in {costliest_flat['society']}. It is priced at ${costliest_flat['price']/10000000} crores and has a rate per square foot of ${costliest_flat['rate_per_sqft']:,}. The flat is currently {costliest_flat['status']} and is built by {costliest_flat['builder_name']}. RERA approval status: {'Approved' if costliest_flat['rera_approval'] else 'Not Approved'}.")   

# Question 2- Which locality has the highest average price?
highest_avg_price_locality = df.groupby('locality')['price'].mean().idxmax()
highest_avg_price = df.groupby("locality")["price"].mean().max()
print(f"the locality with highest average price i.e {highest_avg_price/10000000:.2f} crore is {highest_avg_price_locality}")

# # Question3- Which locality has the highest rate per square foot?
highest_rate_per_sq_foot_locality = df.groupby("locality")["rate_per_sqft"].mean().idxmax()
highest_rate_per_sq_foot = df.groupby("locality")["rate_per_sqft"].mean().max()
print(f"the locality with highest rate per square foot i.e {highest_rate_per_sq_foot:.2f} is {highest_rate_per_sq_foot_locality}")

# # Question4- Do ready-to-move properties cost more than under-construction properties?
ready_to_move_avg_cost = df[df["status"] == "ready to move"]["price"].mean()
under_construction_avg_cost = df[df["status"] == "under construction"]["price"].mean()
if ready_to_move_avg_cost > under_construction_avg_cost:
    print(f"Ready-to-move properties cost more than under-construction properties. Average price of ready-to-move properties is ${ready_to_move_avg_cost/10000000:.2f} crores, while average price of under-construction properties is ${under_construction_avg_cost/10000000:.2f} crores.")
else:
    print(f"Under-construction properties cost more than ready-to-move properties. Average price of under-construction properties is ${under_construction_avg_cost/10000000:.2f} crores, while average price of ready-to-move properties is ${ready_to_move_avg_cost/10000000:.2f} crores.")

# # Question5- Do RERA-approval properties command a price premium?
rera_approved_avg_price = df[df["rera_approval"] == True]["price"].mean()
rera_not_approved_avg_price = df[df["rera_approval"] == False]["price"].mean()
if rera_approved_avg_price > rera_not_approved_avg_price:
    print(f"RERA-approved properties command a price premium. Average price of RERA-approved properties is ${rera_approved_avg_price/10000000:.2f} crores, while average price of non-RERA-approved properties is ${rera_not_approved_avg_price/10000000:.2f} crores.")
else:
    print(f"Non-RERA-approved properties command a price premium. Average price of non-RERA-approved properties is ${rera_not_approved_avg_price/10000000:.2f} crores, while average price of RERA-approved properties is ${rera_approved_avg_price/10000000:.2f} crores.")

# # Question 6: How does area  impact price?
sns.scatterplot(data=df, x="area", y="price")
plt.show()
# area not impact the price from scatter plot

# # Question 7: Which BHK configuration is the most expensive on average based on rate per square feet?
bhk_most_expensive_config = df.groupby("bhk_count")["rate_per_sqft"].mean().idxmax()
print(f"bhk most expensive config is {bhk_most_expensive_config}")


# # Question 8: Which property type (Apartment, Floor, Plot) is the costliest?
most_expensive = df.groupby("flat_type")["price"].mean().idxmax()
most_expensive_avg_price = df.groupby("flat_type")["price"].mean().max()
print(f"Most expensive is {most_expensive} with average price {most_expensive_avg_price:.2f}")

# # Question 9: Do certain builders or companies consistently price higher? Also print top 5 builders name?
price_by_company = df.groupby("company_name")["price"].mean()
top_5_company = price_by_company.sort_values(ascending=False).head(5)
print("top 5 companies that price higher are:", end=" ")
for company in top_5_company.index:
    print(company, end=", ")
    
print(" ")

price_by_builder = df.groupby("builder_name")["price"].mean()
top_5_builder = price_by_builder.sort_values(ascending=False).head(5)
print("top 5 builder that price higher are:", end=" ")
for builder in top_5_builder.index:
    print(builder, end=", ")

# Question9 - Answer - Yes


# Question 10: Are larger homes always more expensive per square foot?
sns.scatterplot(data=df, x="area", y="rate_per_sqft")
plt.show()
# Answer10 - No





