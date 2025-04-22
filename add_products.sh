#!/bin/bash

# Run Flask shell commands to add products to the database
flask shell <<EOF
from app import Product, db


# Create 10 specific product entries
products = [
    Product(title='Product 1', description='Description for Product 1', price=29.99),
    Product(title='Product 2', description='Description for Product 2', price=49.99),
    Product(title='Product 3', description='Description for Product 3', price=19.99),
    Product(title='Product 4', description='Description for Product 4', price=89.99),
    Product(title='Product 5', description='Description for Product 5', price=119.99),
    Product(title='Product 6', description='Description for Product 6', price=159.99),
    Product(title='Product 7', description='Description for Product 7', price=25.99),
    Product(title='Product 8', description='Description for Product 8', price=34.99),
    Product(title='Product 9', description='Description for Product 9', price=99.99),
    Product(title='Product 10', description='Description for Product 10', price=149.99)
]

# Add the products to the session and commit
db.session.add_all(products)
db.session.commit()

# Verify the added products
all_products = Product.query.all()
print(all_products)
EOF
