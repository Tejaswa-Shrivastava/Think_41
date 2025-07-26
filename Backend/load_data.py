"""
Data loading script for populating the database with product data from CSV files
Milestone 2: Database Setup and Data Ingestion
"""
import csv
import os
from sqlalchemy.orm import Session
from backend.database import SessionLocal, create_tables
from backend import models, schemas, crud

def load_products_from_csv(csv_file_path: str):
    """
    Load product data from CSV file into the database
    """
    db = SessionLocal()
    
    try:
        # Create tables if they don't exist
        create_tables()
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            products_loaded = 0
            for row in csv_reader:
                try:
                    # Convert string values to appropriate types
                    product_data = {
                        'name': row.get('name', '').strip(),
                        'category': row.get('category', '').strip() or None,
                        'price': float(row.get('price', 0)) if row.get('price') else None,
                        'description': row.get('description', '').strip() or None,
                        'brand': row.get('brand', '').strip() or None,
                        'sku': row.get('sku', '').strip() or None,
                        'stock_quantity': int(row.get('stock_quantity', 0)) if row.get('stock_quantity') else 0,
                        'rating': float(row.get('rating', 0)) if row.get('rating') else None
                    }
                    
                    # Skip rows with empty names
                    if not product_data['name']:
                        continue
                    
                    # Create product
                    product_schema = schemas.ProductCreate(**product_data)
                    crud.create_product(db, product_schema)
                    products_loaded += 1
                    
                    if products_loaded % 100 == 0:
                        print(f"Loaded {products_loaded} products...")
                        db.commit()
                
                except Exception as e:
                    print(f"Error loading product row: {row}, Error: {e}")
                    continue
            
            db.commit()
            print(f"Successfully loaded {products_loaded} products from {csv_file_path}")
            
    except Exception as e:
        print(f"Error loading data from CSV: {e}")
        db.rollback()
    finally:
        db.close()

def create_sample_users():
    """
    Create sample users for testing
    """
    db = SessionLocal()
    
    try:
        # Check if users already exist
        existing_user = crud.get_user_by_username(db, "demo_user")
        if existing_user:
            print("Sample users already exist")
            return
        
        # Create sample users
        sample_users = [
            schemas.UserCreate(
                username="demo_user",
                email="demo@example.com",
                full_name="Demo User"
            ),
            schemas.UserCreate(
                username="test_user",
                email="test@example.com", 
                full_name="Test User"
            )
        ]
        
        for user_data in sample_users:
            crud.create_user(db, user_data)
        
        db.commit()
        print("Sample users created successfully")
        
    except Exception as e:
        print(f"Error creating sample users: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """
    Main function to run data loading
    """
    print("Starting data loading process...")
    
    # Create tables
    create_tables()
    print("Database tables created/verified")
    
    # Load products from CSV
    csv_file = "backend/sample_products.csv"
    if os.path.exists(csv_file):
        load_products_from_csv(csv_file)
    else:
        print(f"CSV file not found: {csv_file}")
        print("Please ensure the CSV file exists with the following columns:")
        print("name, category, price, description, brand, sku, stock_quantity, rating")
    
    # Create sample users
    create_sample_users()
    
    print("Data loading process completed!")

if __name__ == "__main__":
    main()
