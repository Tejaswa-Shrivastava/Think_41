"""
FastAPI main application
Complete implementation of all milestones:
- Milestone 2: Database Setup and Data Ingestion
- Milestone 3: Data Schemas (Chat History)  
- Milestone 4: Core Chat API
- Milestone 5: LLM Integration and Business Logic
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from backend.database import get_db, create_tables
from backend import crud, models, schemas
from backend.chat_service import ChatService
from backend.config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Conversational AI Backend with Groq LLM Integration"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chat service
chat_service = ChatService()

@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    create_tables()
    print("Database tables created/verified")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "chat": "/api/chat",
            "users": "/api/users",
            "products": "/api/products",
            "search": "/api/products/search?q=query",
            "stats": "/api/stats"
        },
        "database": {
            "users": "2 demo users created",
            "products": "20 products loaded from CSV",
            "ready": True
        },
        "ai_integration": {
            "provider": "xAI (Grok)",
            "model": settings.GROQ_MODEL,
            "status": "configured" if settings.GROQ_API_KEY else "needs_api_key"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": settings.APP_NAME}

# User endpoints
@app.post("/api/users", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    # Check if username already exists
    existing_user = crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    return crud.create_user(db, user)

@app.get("/api/users/{user_id}", response_model=schemas.User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

# Product endpoints
@app.get("/api/products", response_model=List[schemas.Product])
async def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of products"""
    return crud.get_products(db, skip=skip, limit=limit)

@app.get("/api/products/search")
async def search_products(q: str, db: Session = Depends(get_db)):
    """Search products by query"""
    if not q or len(q.strip()) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Search query must be at least 2 characters long"
        )
    return crud.search_products(db, q)

@app.get("/api/products/{product_id}", response_model=schemas.Product)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get product by ID"""
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

# Conversation endpoints
@app.get("/api/users/{user_id}/conversations", response_model=List[schemas.Conversation])
async def get_user_conversations(user_id: int, db: Session = Depends(get_db)):
    """Get all conversations for a user"""
    # Verify user exists
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return crud.get_user_conversations(db, user_id)

@app.get("/api/conversations/{conversation_id}", response_model=schemas.Conversation)
async def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    """Get conversation by ID"""
    conversation = crud.get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    return conversation

@app.get("/api/conversations/{conversation_id}/messages", response_model=List[schemas.Message])
async def get_conversation_messages(conversation_id: int, db: Session = Depends(get_db)):
    """Get all messages for a conversation"""
    conversation = crud.get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    return crud.get_conversation_messages(db, conversation_id)

# Milestone 4: Core Chat API
@app.post("/api/chat", response_model=schemas.ChatResponse)
async def chat(chat_request: schemas.ChatRequest, db: Session = Depends(get_db)):
    """
    Main chat endpoint - handles user messages and generates AI responses
    Milestone 4: Core Chat API
    Milestone 5: LLM Integration and Business Logic
    """
    try:
        # Verify user exists
        user = crud.get_user(db, chat_request.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Validate message content
        if not chat_request.message or not chat_request.message.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message content cannot be empty"
            )
        
        # Process chat message through the service
        result = chat_service.process_chat_message(
            db=db,
            user_id=chat_request.user_id,
            message=chat_request.message.strip(),
            conversation_id=chat_request.conversation_id
        )
        
        return schemas.ChatResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"Chat error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your message"
        )

# Additional endpoints for debugging and administration
@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get application statistics"""
    user_count = db.query(models.User).count()
    product_count = db.query(models.Product).count()
    conversation_count = db.query(models.Conversation).count()
    message_count = db.query(models.Message).count()
    
    return {
        "users": user_count,
        "products": product_count,
        "conversations": conversation_count,
        "messages": message_count
    }

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
