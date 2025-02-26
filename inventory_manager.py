import sqlite3

# Connect to SQLite database (it will create the file if it doesn't exist)
connection = sqlite3.connect('inventory.db')

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Create the products table if it doesn't already exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    quantity INTEGER,
    price REAL,
    supplier TEXT
)
''')

# Commit changes
connection.commit()

# Function to add a new product
def add_product(name, category, quantity, price, supplier):
    cursor.execute('''
    INSERT INTO products (name, category, quantity, price, supplier)
    VALUES (?, ?, ?, ?, ?)
    ''', (name, category, quantity, price, supplier))
    connection.commit()
    print(f"\nProduct '{name}' added successfully!")

# Function to view all products
def view_products():
    print("\nViewing All Products:")
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    if products:
        for product in products:
            print(f"\nProduct ID: {product[0]}")
            print(f"Name: {product[1]}")
            print(f"Category: {product[2]}")
            print(f"Quantity: {product[3]}")
            print(f"Price: ${product[4]:.2f}")
            print(f"Supplier: {product[5]}")
    else:
        print("No products found.")

# Function to search for a product by name
def search_product(name):
    print("\nSearch Instructions:")
    print("You can search for a product by its name or part of the name.")
    print("For example, if you're searching for 'Laptop', you can enter 'Lap' or 'top'.")
    print("The program will find products that contain the search term anywhere in the name.")
    
    cursor.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + name + '%',))
    products = cursor.fetchall()
    if products:
        for product in products:
            print(f"\nProduct ID: {product[0]}")
            print(f"Name: {product[1]}")
            print(f"Category: {product[2]}")
            print(f"Quantity: {product[3]}")
            print(f"Price: ${product[4]:.2f}")
            print(f"Supplier: {product[5]}")
    else:
        print(f"No products found with the name '{name}'.")

# Function to update an existing product
def update_product(id, name=None, category=None, quantity=None, price=None, supplier=None):
    if name:
        cursor.execute("UPDATE products SET name = ? WHERE id = ?", (name, id))
    if category:
        cursor.execute("UPDATE products SET category = ? WHERE id = ?", (category, id))
    if quantity is not None:
        cursor.execute("UPDATE products SET quantity = ? WHERE id = ?", (quantity, id))
    if price is not None:
        cursor.execute("UPDATE products SET price = ? WHERE id = ?", (price, id))
    if supplier:
        cursor.execute("UPDATE products SET supplier = ? WHERE id = ?", (supplier, id))
    connection.commit()
    print(f"\nProduct ID {id} updated successfully!")

# Function to delete a product
def delete_product(id):
    cursor.execute("DELETE FROM products WHERE id = ?", (id,))
    connection.commit()
    print(f"\nProduct ID {id} deleted successfully!")

# Function to update the quantity of a product (e.g., when products are sold or restocked)
def update_quantity(id, quantity):
    cursor.execute("UPDATE products SET quantity = quantity + ? WHERE id = ?", (quantity, id))
    connection.commit()
    print(f"\nQuantity of Product ID {id} updated successfully!")

# Main program to interact with the user
def main():
    while True:
        print("\nInventory Management System")
        print("1. Add a Product")
        print("2. View All Products")
        print("3. Search for a Product")
        print("4. Update a Product")
        print("5. Delete a Product")
        print("6. Update Product Quantity")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ")
        
        if choice == '1':
            print("\nTo add a product, provide the following details:")
            name = input("Enter product name: ")
            category = input("Enter category: ")
            quantity = int(input("Enter quantity: "))
            price = float(input("Enter price per unit: "))
            supplier = input("Enter supplier name: ")
            add_product(name, category, quantity, price, supplier)
        
        elif choice == '2':
            view_products()
        
        elif choice == '3':
            print("\nSearch Instructions:")
            print("You can search for a product by its name or part of the name.")
            print("For example, if you're searching for 'Laptop', you can enter 'Lap' or 'top'.")
            print("The program will find products that contain the search term anywhere in the name.")
            name = input("Enter the product name or part of the name to search for: ")
            search_product(name)
        
        elif choice == '4':
            print("\nTo update a product, provide the following details (leave blank to keep current values):")
            id = int(input("Enter the product ID to update: "))
            name = input("Enter new name (leave blank to keep current): ")
            category = input("Enter new category (leave blank to keep current): ")
            quantity = input("Enter new quantity (leave blank to keep current): ")
            price = input("Enter new price (leave blank to keep current): ")
            supplier = input("Enter new supplier (leave blank to keep current): ")
            update_product(id, name, category, quantity if quantity else None, 
                           price if price else None, supplier if supplier else None)
        
        elif choice == '5':
            id = int(input("Enter the product ID to delete: "))
            delete_product(id)
        
        elif choice == '6':
            id = int(input("Enter the product ID to update quantity: "))
            quantity = int(input("Enter the quantity to add/subtract (negative for subtraction): "))
            update_quantity(id, quantity)
        
        elif choice == '7':
            print("\nExiting the program. Goodbye!")
            break
        
        else:
            print("\nInvalid choice. Please enter a number between 1 and 7.")

# Run the program
main()

# Close the connection when done
connection.close()