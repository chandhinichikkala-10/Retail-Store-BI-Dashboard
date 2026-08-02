import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker("en_IN")

# Product Details
products = {
    "Groceries": {
        "Rice": 60,
        "Wheat Flour": 45,
        "Sugar": 50,
        "Cooking Oil": 180,
        "Salt": 25
    },
    "Beverages": {
        "Tea": 220,
        "Coffee": 350,
        "Juice": 90,
        "Soft Drink": 60
    },
    "Dairy": {
        "Milk": 55,
        "Butter": 250,
        "Cheese": 400,
        "Curd": 45
    },
    "Personal Care": {
        "Shampoo": 280,
        "Soap": 40,
        "Toothpaste": 120,
        "Face Wash": 180
    },
    "Bakery": {
        "Bread": 40,
        "Biscuits": 35,
        "Cake": 350
    },
    "Snacks": {
        "Chips": 20,
        "Cookies": 80,
        "Namkeen": 60
    },
    "Stationery": {
        "Notebook": 80,
        "Pen": 15,
        "Pencil": 10
    }
}

regions = ["North", "South", "East", "West"]

payment_modes = [
    "UPI",
    "Cash",
    "Credit Card",
    "Debit Card"
]

salespersons = [
    "Priya", "Rahul", "Sneha", "Arjun", "Anjali",
    "Kiran", "Neha", "Vikram", "Pooja", "Ramesh"
]

# Generate random date
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)

def random_date():
    delta = end_date - start_date
    return start_date + timedelta(days=random.randint(0, delta.days))

records = []

for i in range(1, 351):

    category = random.choice(list(products.keys()))
    product = random.choice(list(products[category].keys()))

    unit_price = products[category][product]

    quantity = random.randint(1, 10)

    revenue = quantity * unit_price

    cost = round(revenue * random.uniform(0.60, 0.85), 2)

    profit = round(revenue - cost, 2)

    stock = random.randint(0, 300)

    if stock > 150:
        inventory = "In Stock"
    elif stock >= 50:
        inventory = "Low Stock"
    else:
        inventory = "Out of Stock"

    rating = round(random.uniform(3.5, 5.0), 1)

    order_date = random_date()

    record = {
        "Order_ID": f"ORD{i:04}",
        "Order_Date": order_date.strftime("%Y-%m-%d"),
        "Customer_ID": f"C{random.randint(1,100):03}",
        "Customer_Name": fake.name(),
        "Product_ID": f"P{random.randint(1,25):03}",
        "Product_Name": product,
        "Category": category,
        "Region": random.choice(regions),
        "Quantity_Sold": quantity,
        "Unit_Price": unit_price,
        "Revenue": revenue,
        "Cost": cost,
        "Profit": profit,
        "Current_Stock": stock,
        "Inventory_Status": inventory,
        "Customer_Rating": rating,
        "Payment_Mode": random.choice(payment_modes),
        "Salesperson": random.choice(salespersons)
    }

    records.append(record)

df = pd.DataFrame(records)

df.to_csv("Retail_Store_Sales.csv", index=False)

print("Dataset Created Successfully!")
print(df.head())