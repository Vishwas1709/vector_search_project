import csv
import random

electronics = [
    "Apple iPhone 14 Pro", "Apple iPhone 14",
    "Samsung Galaxy S22 Ultra", "Samsung Galaxy S22",
    "HP Pavilion Laptop", "Dell Inspiron 15",
    "Sony WH-1000XM4 Headphones", "Apple AirPods Pro"
]

electronics_typos = [
    "Samzung Galaxy S21",
    "Aple iPhone 14",
    "Del Inspiron 155",
    "Soni WH-1000XM4"
]

fashion = [
    "Nike Air Max Shoes", "Adidas Ultraboost",
    "Puma Sports T-Shirt", "Levis 501 Jeans",
    "Zara Slim Fit Shirt"
]

groceries = [
    "Organic Apple 1kg", "Fresh Milk 1L",
    "Brown Bread 400g", "Fortune Sunflower Oil 1L",
    "Aashirvaad Atta 5kg"
]

all_products = electronics + electronics_typos + fashion + groceries

while len(all_products) < 500:
    category = random.choice([electronics, fashion, groceries])
    all_products.append(random.choice(category))

with open("products.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["product_id", "product_name"])
    for i, name in enumerate(all_products):
        writer.writerow([i+1, name])

print("products.csv generated successfully!")
