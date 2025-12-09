"""
FastAPI backend for AI Agent Chatbot.
Provides REST API endpoints for the React frontend.
"""

import logging
import uuid
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import get_settings
from utils import setup_logging
from chatbot import ChatbotAgent
from chatbot.state import create_initial_state, ConversationState

# Setup logging
settings = get_settings()
setup_logging(settings.log_level)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Agent Chatbot API",
    description="REST API for conversational CRUD operations",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite and CRA default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global chatbot agent and session storage
chatbot_agent = ChatbotAgent()
conversation_sessions: Dict[str, ConversationState] = {}

logger.info("FastAPI backend initialized")


# Request/Response models
class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    session_id: str


class ClearRequest(BaseModel):
    session_id: str


class HealthResponse(BaseModel):
    status: str
    message: str


# API Endpoints
@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint."""
    return HealthResponse(
        status="success",
        message="AI Agent Chatbot API is running"
    )


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="success",
        message="API is healthy"
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process chat message and return response.
    
    Args:
        request: ChatRequest containing message and optional session_id
        
    Returns:
        ChatResponse with bot response and session_id
    """
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Get or create conversation state
        if session_id not in conversation_sessions:
            conversation_sessions[session_id] = create_initial_state()
            logger.info(f"Created new session: {session_id}")
        
        state = conversation_sessions[session_id]
        
        # Process message through chatbot agent
        logger.info(f"Processing message for session {session_id}: {request.message[:50]}...")
        response, updated_state = chatbot_agent.chat(request.message, state)
        
        # Update session state
        conversation_sessions[session_id] = updated_state
        
        return ChatResponse(
            response=response,
            session_id=session_id
        )
        
    except Exception as e:
        logger.error(f"Error processing chat: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing message: {str(e)}"
        )


@app.post("/api/clear")
async def clear_conversation(request: ClearRequest):
    """
    Clear conversation history for a session.
    
    Args:
        request: ClearRequest containing session_id
        
    Returns:
        Success message
    """
    try:
        session_id = request.session_id
        
        if session_id in conversation_sessions:
            del conversation_sessions[session_id]
            logger.info(f"Cleared session: {session_id}")
            
        return {
            "status": "success",
            "message": "Conversation cleared"
        }
        
    except Exception as e:
        logger.error(f"Error clearing conversation: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing conversation: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting FastAPI server...")
    logger.info(f"Using model: {settings.gemini_model}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
