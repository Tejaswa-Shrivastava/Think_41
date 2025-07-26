"""
CRUD operations for database models
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List
from backend import models, schemas

# Product CRUD operations
def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    """Create a new product"""
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int) -> Optional[models.Product]:
    """Get a product by ID"""
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[models.Product]:
    """Get list of products"""
    return db.query(models.Product).offset(skip).limit(limit).all()

def search_products(db: Session, query: str) -> List[models.Product]:
    """Search products by name, category, or brand"""
    search_term = f"%{query}%"
    return db.query(models.Product).filter(
        (models.Product.name.ilike(search_term)) |
        (models.Product.category.ilike(search_term)) |
        (models.Product.brand.ilike(search_term)) |
        (models.Product.description.ilike(search_term))
    ).all()

# User CRUD operations
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user"""
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """Get a user by ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """Get a user by username"""
    return db.query(models.User).filter(models.User.username == username).first()

# Conversation CRUD operations
def create_conversation(db: Session, conversation: schemas.ConversationCreate) -> models.Conversation:
    """Create a new conversation"""
    db_conversation = models.Conversation(**conversation.model_dump())
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

def get_conversation(db: Session, conversation_id: int) -> Optional[models.Conversation]:
    """Get a conversation by ID"""
    return db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()

def get_user_conversations(db: Session, user_id: int) -> List[models.Conversation]:
    """Get all conversations for a user"""
    return db.query(models.Conversation).filter(
        models.Conversation.user_id == user_id
    ).order_by(desc(models.Conversation.updated_at)).all()

# Message CRUD operations
def create_message(db: Session, message: schemas.MessageCreate) -> models.Message:
    """Create a new message"""
    db_message = models.Message(**message.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_conversation_messages(db: Session, conversation_id: int) -> List[models.Message]:
    """Get all messages for a conversation in chronological order"""
    return db.query(models.Message).filter(
        models.Message.conversation_id == conversation_id
    ).order_by(models.Message.timestamp).all()
