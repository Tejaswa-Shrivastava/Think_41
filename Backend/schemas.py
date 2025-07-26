"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

# Product schemas
class ProductBase(BaseModel):
    name: str
    category: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    brand: Optional[str] = None
    sku: Optional[str] = None
    stock_quantity: Optional[int] = 0
    rating: Optional[float] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    created_at: datetime

# Message schemas
class MessageBase(BaseModel):
    content: str
    is_user_message: bool

class MessageCreate(MessageBase):
    conversation_id: int

class Message(MessageBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    conversation_id: int
    timestamp: datetime

# Conversation schemas
class ConversationBase(BaseModel):
    title: Optional[str] = "New Conversation"

class ConversationCreate(ConversationBase):
    user_id: int

class Conversation(ConversationBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    messages: List[Message] = []

# Chat API schemas
class ChatRequest(BaseModel):
    user_id: int
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    conversation_id: int
    user_message: Message
    ai_message: Message
    messages: List[Message]
