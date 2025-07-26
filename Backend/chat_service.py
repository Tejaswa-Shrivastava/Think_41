"""
Chat service for handling LLM integration and business logic
Milestone 5: LLM Integration and Business Logic
"""
import os
import json
from typing import Optional, Dict, Any
from openai import OpenAI
from sqlalchemy.orm import Session
from backend import crud, models, schemas
from backend.config import settings

class ChatService:
    """
    Service class for handling chat functionality with Groq LLM integration
    """
    
    def __init__(self):
        # Initialize xAI client using OpenAI-compatible interface
        self.client = OpenAI(
            base_url="https://api.x.ai/v1",
            api_key=settings.GROQ_API_KEY
        )
        self.model = settings.GROQ_MODEL
    
    def process_chat_message(
        self, 
        db: Session, 
        user_id: int, 
        message: str, 
        conversation_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Process a chat message through the complete pipeline:
        1. Save user message to DB
        2. Generate AI response using LLM
        3. Save AI response to DB
        4. Return complete conversation context
        """
        
        # Get or create conversation
        if conversation_id:
            conversation = crud.get_conversation(db, conversation_id)
            if not conversation or conversation.user_id != user_id:
                raise ValueError("Invalid conversation ID or access denied")
        else:
            # Create new conversation
            conversation_data = schemas.ConversationCreate(
                user_id=user_id,
                title=self._generate_conversation_title(message)
            )
            conversation = crud.create_conversation(db, conversation_data)
        
        # Save user message
        user_message_data = schemas.MessageCreate(
            conversation_id=int(conversation.id),
            content=message,
            is_user_message=True
        )
        user_message = crud.create_message(db, user_message_data)
        
        # Get conversation history for context
        conversation_history = crud.get_conversation_messages(db, int(conversation.id))
        
        # Generate AI response
        ai_response = self._generate_ai_response(db, conversation_history, message)
        
        # Save AI message
        ai_message_data = schemas.MessageCreate(
            conversation_id=int(conversation.id),
            content=ai_response,
            is_user_message=False
        )
        ai_message = crud.create_message(db, ai_message_data)
        
        # Get updated conversation messages
        updated_messages = crud.get_conversation_messages(db, int(conversation.id))
        
        return {
            "conversation_id": int(conversation.id),
            "user_message": user_message,
            "ai_message": ai_message,
            "messages": updated_messages
        }
    
    def _generate_ai_response(self, db: Session, conversation_history: list, current_message: str) -> str:
        """
        Generate AI response using Groq LLM with business logic
        """
        try:
            # Build conversation context
            messages = [
                {
                    "role": "system",
                    "content": self._get_system_prompt()
                }
            ]
            
            # Add conversation history
            for msg in conversation_history[:-1]:  # Exclude the current message
                role = "user" if msg.is_user_message else "assistant"
                messages.append({
                    "role": role,
                    "content": msg.content
                })
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": current_message
            })
            
            # Check if we need to query product database
            product_context = self._get_product_context(db, current_message)
            if product_context:
                messages.append({
                    "role": "system",
                    "content": f"Relevant product information: {product_context}"
                })
            
            # Call xAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content or "I apologize, but I couldn't generate a response. Please try again."
            
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again later."
    
    def _get_system_prompt(self) -> str:
        """
        Get the system prompt for the AI assistant
        """
        return """
        You are a helpful e-commerce assistant. Your role is to:
        
        1. Help customers find products they're looking for
        2. Answer questions about products, pricing, and availability
        3. Ask clarifying questions when needed to better understand customer needs
        4. Provide detailed product recommendations based on customer preferences
        5. Be friendly, professional, and informative
        
        If you don't have enough information about what the customer is looking for, ask clarifying questions.
        When you have relevant product information available, use it to provide specific recommendations.
        
        Always be helpful and try to guide the customer towards finding what they need.
        """
    
    def _get_product_context(self, db: Session, message: str) -> Optional[str]:
        """
        Search for relevant products based on the message content and return context
        """
        try:
            # Simple keyword extraction for product search
            products = crud.search_products(db, message)
            
            if not products:
                return None
            
            # Limit to top 5 most relevant products
            products = products[:5]
            
            context_parts = []
            for product in products:
                context_parts.append(
                    f"- {product.name} ({product.brand}) - ${product.price:.2f} - {product.category} - Stock: {product.stock_quantity} - Rating: {product.rating}/5"
                )
            
            return "Available products:\n" + "\n".join(context_parts)
            
        except Exception as e:
            print(f"Error getting product context: {e}")
            return None
    
    def _generate_conversation_title(self, first_message: str) -> str:
        """
        Generate a title for the conversation based on the first message
        """
        # Simple title generation - could be enhanced with LLM
        words = first_message.split()[:5]
        title = " ".join(words)
        if len(title) > 50:
            title = title[:47] + "..."
        return title or "New Conversation"
