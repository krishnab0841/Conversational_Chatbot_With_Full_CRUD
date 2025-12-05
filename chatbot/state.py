"""
Conversation state management for the LangGraph agent.
Defines the state structure used throughout the conversation flow.
"""

from typing import TypedDict, Literal, Optional, Dict, Any, List
from datetime import date


class ConversationState(TypedDict):
    """State maintained throughout the conversation."""
    
    # Conversation management
    messages: List[Dict[str, str]]  # List of {'role': 'user'/'assistant', 'content': str}
    current_intent: Optional[str]  # create, read, update, delete, help, exit
    
    # User identification
    user_email: Optional[str]  # Email for identifying user
    
    # Data collection for operations
    collecting_field: Optional[str]  # Current field being collected
    user_data: Dict[str, Any]  # Collected user data
    
    # Operation status
    operation_complete: bool  # Whether current operation is complete
    error_message: Optional[str]  # Any error that occurred
    
    # Next action
    next_action: Optional[str]  # Next node to execute


def create_initial_state() -> ConversationState:
    """
    Create initial conversation state.
    
    Returns:
        Initial ConversationState
    """
    return ConversationState(
        messages=[],
        current_intent=None,
        user_email=None,
        collecting_field=None,
        user_data={},
        operation_complete=False,
        error_message=None,
        next_action=None
    )
