#!/usr/bin/env python3
import os
import csv
import psycopg2
from psycopg2.extras import RealDictCursor
import uuid
from datetime import datetime

def load_csv_to_products():
    """
    Load data from CSV files to the products table.
    This script expects CSV files in a 'data' directory with product information.
    """
    
    # Get database URL from environment
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("ERROR: DATABASE_URL environment variable not set")
        return
    
    try:
        # Connect to database
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Create products table if it doesn't exist
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS products (
            id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid(),
            name TEXT NOT NULL,
            description TEXT,
            price DECIMAL(10, 2),
            category TEXT,
            brand TEXT,
            in_stock BOOLEAN DEFAULT true,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """
        cursor.execute(create_table_sql)
        
        # Look for CSV files in data directory
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        csv_files = []
        
        if os.path.exists(data_dir):
            csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        
        if not csv_files:
            print("No CSV files found in data directory. Creating sample data...")
            # Create sample product data
            sample_products = [
                {
                    'name': 'ASUS VivoBook 15',
                    'description': 'Intel i5, 8GB RAM, 512GB SSD - Perfect for students and professionals',
                    'price': 749.99,
                    'category': 'Laptops',
                    'brand': 'ASUS',
                    'in_stock': True
                },
                {
                    'name': 'Lenovo IdeaPad 3',
                    'description': 'AMD Ryzen 5, 8GB RAM, 256GB SSD - Great value laptop',
                    'price': 649.99,
                    'category': 'Laptops',
                    'brand': 'Lenovo',
                    'in_stock': True
                },
                {
                    'name': 'HP Pavilion 15',
                    'description': 'Intel i7, 16GB RAM, 1TB SSD - High performance laptop',
                    'price': 899.99,
                    'category': 'Laptops',
                    'brand': 'HP',
                    'in_stock': True
                },
                {
                    'name': 'Dell XPS 13',
                    'description': 'Intel i7, 16GB RAM, 512GB SSD - Premium ultrabook',
                    'price': 1299.99,
                    'category': 'Laptops',
                    'brand': 'Dell',
                    'in_stock': True
                },
                {
                    'name': 'MacBook Air M2',
                    'description': 'Apple M2 chip, 8GB RAM, 256GB SSD - Latest Apple laptop',
                    'price': 1199.99,
                    'category': 'Laptops',
                    'brand': 'Apple',
                    'in_stock': True
                },
                {
                    'name': 'Logitech MX Master 3',
                    'description': 'Wireless mouse with advanced precision and customization',
                    'price': 99.99,
                    'category': 'Accessories',
                    'brand': 'Logitech',
                    'in_stock': True
                },
                {
                    'name': 'Mechanical Keyboard RGB',
                    'description': 'Gaming mechanical keyboard with RGB lighting',
                    'price': 149.99,
                    'category': 'Accessories',
                    'brand': 'Corsair',
                    'in_stock': True
                },
                {
                    'name': 'Sony WH-1000XM4',
                    'description': 'Wireless noise-canceling headphones',
                    'price': 349.99,
                    'category': 'Audio',
                    'brand': 'Sony',
                    'in_stock': True
                },
                {
                    'name': 'Samsung 27" 4K Monitor',
                    'description': '4K UHD monitor with HDR support',
                    'price': 329.99,
                    'category': 'Monitors',
                    'brand': 'Samsung',
                    'in_stock': True
                },
                {
                    'name': 'External SSD 1TB',
                    'description': 'Portable SSD with USB-C connectivity',
                    'price': 129.99,
                    'category': 'Storage',
                    'brand': 'SanDisk',
                    'in_stock': True
                }
            ]
            
            # Insert sample products
            for product in sample_products:
                insert_sql = """
                INSERT INTO products (name, description, price, category, brand, in_stock)
                VALUES (%(name)s, %(description)s, %(price)s, %(category)s, %(brand)s, %(in_stock)s);
                """
                try:
                    cursor.execute(insert_sql, product)
                except Exception as e:
                    if "duplicate key" not in str(e).lower():
                        raise e
            
            conn.commit()
            print(f"Inserted {len(sample_products)} sample products")
        
        else:
            # Process CSV files
            total_inserted = 0
            for csv_file in csv_files:
                csv_path = os.path.join(data_dir, csv_file)
                print(f"Processing {csv_file}...")
                
                with open(csv_path, 'r', encoding='utf-8') as file:
                    csv_reader = csv.DictReader(file)
                    batch_size = 100
                    batch = []
                    
                    for row in csv_reader:
                        # Map CSV columns to database columns
                        product = {
                            'name': row.get('name', row.get('product_name', '')),
                            'description': row.get('description', row.get('desc', '')),
                            'price': float(row.get('price', 0)) if row.get('price') else None,
                            'category': row.get('category', row.get('type', '')),
                            'brand': row.get('brand', row.get('manufacturer', '')),
                            'in_stock': row.get('in_stock', 'true').lower() == 'true'
                        }
                        
                        batch.append(product)
                        
                        if len(batch) >= batch_size:
                            # Insert batch
                            insert_sql = """
                            INSERT INTO products (name, description, price, category, brand, in_stock)
                            VALUES (%(name)s, %(description)s, %(price)s, %(category)s, %(brand)s, %(in_stock)s);
                            """
                            for product in batch:
                                try:
                                    cursor.execute(insert_sql, product)
                                except Exception as e:
                                    if "duplicate key" not in str(e).lower():
                                        raise e
                            conn.commit()
                            total_inserted += len(batch)
                            batch = []
                    
                    # Insert remaining items
                    if batch:
                        for product in batch:
                            try:
                                cursor.execute(insert_sql, product)
                            except Exception as e:
                                if "duplicate key" not in str(e).lower():
                                    raise e
                        conn.commit()
                        total_inserted += len(batch)
                
                print(f"Processed {csv_file}")
            
            print(f"Total products inserted: {total_inserted}")
        
        # Get final count
        cursor.execute("SELECT COUNT(*) FROM products;")
        count = cursor.fetchone()[0]
        print(f"Total products in database: {count}")
        
        cursor.close()
        conn.close()
        print("Database loading completed successfully!")
        
    except Exception as e:
        print(f"Error loading data: {e}")
        if 'conn' in locals():
            conn.rollback()
            cursor.close()
            conn.close()

if __name__ == "__main__":
    load_csv_to_products()
