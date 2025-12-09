"""
LangGraph-based conversational agent for CRUD operations.
Manages the conversation flow for user registration operations.
"""

import logging
from typing import Dict, Any, Literal
from datetime import date

from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from .state import ConversationState, create_initial_state
from database import UserRepository
from database.models import User, UserUpdate
from utils.validators import validate_email, validate_phone, validate_date, extract_field_from_message
from config import get_settings

logger = logging.getLogger(__name__)


class ChatbotAgent:
    """LangGraph-based chatbot agent for user registration CRUD operations."""
    
    # Fields required for user registration
    REQUIRED_FIELDS = {
        "full_name": "Full Name",
        "email": "Email Address",
        "phone_number": "Phone Number",
        "date_of_birth": "Date of Birth (YYYY-MM-DD)",
        "address": "Full Address"
    }
    
    UPDATEABLE_FIELDS = {
        "full_name": "Full Name",
        "email": "Email Address",
        "phone_number": "Phone Number",
        "date_of_birth": "Date of Birth",
        "address": "Address"
    }
    
    def __init__(self):
        """Initialize the chatbot agent."""
        self.settings = get_settings()
        self.repository = UserRepository()
        
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model=self.settings.gemini_model,
            temperature=self.settings.temperature,
            google_api_key=self.settings.google_api_key
        )
        
        # Build conversation graph
        self.graph = self._build_graph()
        
        logger.info("Chatbot agent initialized")
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph conversation flow."""
        workflow = StateGraph(ConversationState)
        
        # Add nodes
        workflow.add_node("classify_intent", self.classify_intent_node)
        workflow.add_node("handle_create", self.handle_create_node)
        workflow.add_node("handle_read", self.handle_read_node)
        workflow.add_node("handle_update", self.handle_update_node)
        workflow.add_node("handle_delete", self.handle_delete_node)
        workflow.add_node("handle_help", self.handle_help_node)
        workflow.add_node("collect_data", self.collect_data_node)
        workflow.add_node("execute_operation", self.execute_operation_node)
        
        # Set entry point with conditional routing
        workflow.set_entry_point("classify_intent")
        
        # Route based on whether we're already collecting data
        def route_from_classify(state):
            # If we're already collecting data, skip to collect_data
            if state.get("collecting_field"):
                return "collect_data"
            return state.get("current_intent", "help")
        
        # Add conditional edges from classify_intent
        workflow.add_conditional_edges(
            "classify_intent",
            route_from_classify,
            {
                "collect_data": "collect_data",
                "create": "handle_create",
                "read": "handle_read",
                "update": "handle_update",
                "delete": "handle_delete",
                "help": "handle_help",
                "exit": END
            }
        )
        
        # Create flow - go to END after asking first question
        workflow.add_edge("handle_create", END)
        
        # Read flow
        workflow.add_conditional_edges(
            "handle_read",
            lambda state: "execute_operation" if state.get("user_email") else END
        )
        
        # Update flow
        workflow.add_edge("handle_update", END)
        
        # Delete flow
        workflow.add_conditional_edges(
            "handle_delete",
            lambda state: "execute_operation" if state.get("user_email") else END
        )
        
        # Help always ends
        workflow.add_edge("handle_help", END)
        
        # Data collection flow
        workflow.add_conditional_edges(
            "collect_data",
            lambda state: "execute_operation" if state.get("operation_complete") else END
        )
        
        # Execute operation always ends
        workflow.add_edge("execute_operation", END)
        
        return workflow.compile()
    
    def classify_intent_node(self, state: ConversationState) -> ConversationState:
        """Classify user intent from the latest message."""
        if not state["messages"]:
            return state
        
        last_message = state["messages"][-1]["content"].lower()
        
        # Simple keyword-based intent classification
        if any(word in last_message for word in ["create", "register", "sign up", "new account", "new registration"]):
            state["current_intent"] = "create"
        elif any(word in last_message for word in ["read", "show", "view", "get", "retrieve", "my data", "my info"]):
            state["current_intent"] = "read"
        elif any(word in last_message for word in ["update", "change", "modify", "edit"]):
            state["current_intent"] = "update"
        elif any(word in last_message for word in ["delete", "remove", "deregister"]):
            state["current_intent"] = "delete"
        elif any(word in last_message for word in ["help", "what can you do", "commands"]):
            state["current_intent"] = "help"
        elif any(word in last_message for word in ["exit", "quit", "bye", "goodbye"]):
            state["current_intent"] = "exit"
        else:
            # Use LLM for complex intent classification
            state["current_intent"] = self._llm_classify_intent(last_message)
        
        logger.info(f"Classified intent: {state['current_intent']}")
        return state
    
    def _llm_classify_intent(self, message: str) -> str:
        """Use LLM to classify intent when keywords don't match."""
        prompt = f"""Classify the following user message into one of these intents:
- create: User wants to create a new registration
- read: User wants to view their registration data
- update: User wants to update their registration
- delete: User wants to delete their registration
- help: User needs help or asks what you can do
- exit: User wants to end the conversation

User message: "{message}"

Respond with ONLY the intent name (create/read/update/delete/help/exit)."""

        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            intent = response.content.strip().lower()
            
            if intent in ["create", "read", "update", "delete", "help", "exit"]:
                return intent
            
            return "help"  # Default to help if unclear
            
        except Exception as e:
            logger.error(f"LLM intent classification failed: {e}")
            return "help"
    
    def route_intent(self, state: ConversationState) -> str:
        """Route to appropriate handler based on intent."""
        return state.get("current_intent", "help")
    
    def handle_create_node(self, state: ConversationState) -> ConversationState:
        """Handle user creation flow."""
        if not state["user_data"]:
            # First time - needs to collect all fields
            state["collecting_field"] = "full_name"
            state["messages"].append({
                "role": "assistant",
                "content": "I'll help you create a new registration. Let's start!\n\nWhat is your full name?"
            })
        
        return state
    
    def handle_read_node(self, state: ConversationState) -> ConversationState:
        """Handle read operation."""
        if not state.get("user_email"):
            state["collecting_field"] = "email"
            state["messages"].append({
                "role": "assistant",
                "content": "I'll retrieve your registration details. What is your email address?"
            })
        else:
            state["operation_complete"] = True
        
        return state
    
    def handle_update_node(self, state: ConversationState) -> ConversationState:
        """Handle update operation."""
        if not state.get("user_email"):
            state["collecting_field"] = "email"
            state["messages"].append({
                "role": "assistant",
                "content": "I'll help you update your registration. First, what is your email address?"
            })
        elif not state["user_data"].get("update_field"):
            # Ask which field to update
            fields_list = "\n".join([f"- {v}" for v in self.UPDATEABLE_FIELDS.values()])
            state["messages"].append({
                "role": "assistant",
                "content": f"Which field would you like to update?\n\n{fields_list}"
            })
            state["collecting_field"] = "update_field"
        else:
            state["operation_complete"] = True
        
        return state
    
    def handle_delete_node(self, state: ConversationState) -> ConversationState:
        """Handle delete operation."""
        if not state.get("user_email"):
            state["collecting_field"] = "email"
            state["messages"].append({
                "role": "assistant",
                "content": "I'll help you delete your registration. What is your email address?"
            })
        else:
            state["operation_complete"] = True
        
        return state
    
    def handle_help_node(self, state: ConversationState) -> ConversationState:
        """Provide help information."""
        help_message = """I'm your AI registration assistant! I can help you with:

🆕 **Create Registration** - Register with your details
📖 **Read Registration** - View your existing registration
✏️ **Update Registration** - Modify your registration details
🗑️ **Delete Registration** - Remove your registration

To get started, just tell me what you'd like to do. For example:
- "I want to create a new registration"
- "Show me my registration details"
- "I need to update my phone number"
- "Delete my registration"

What would you like to do?"""
        
        state["messages"].append({
            "role": "assistant",
            "content": help_message
        })
        
        return state
    
    def collect_data_node(self, state: ConversationState) -> ConversationState:
        """Collect required data from user."""
        if not state["messages"] or state["messages"][-1]["role"] == "assistant":
            return state
        
        user_message = state["messages"][-1]["content"]
        current_field = state.get("collecting_field")
        
        if not current_field:
            return state
        
        # Validate and store the field
        is_valid, error_msg, processed_value = self._validate_field(current_field, user_message)
        
        if not is_valid:
            state["messages"].append({
                "role": "assistant",
                "content": f"❌ {error_msg}\n\nPlease provide a valid {self.REQUIRED_FIELDS.get(current_field, current_field)}:"
            })
            return state
        
        # Store validated data
        if current_field == "email" and state["current_intent"] == "create":
            # Check if email already exists
            existing_user = self.repository.get_by_email(processed_value)
            if existing_user:
                state["error_message"] = f"Email {processed_value} is already registered."
                state["messages"].append({
                    "role": "assistant",
                    "content": f"❌ Email {processed_value} is already registered. Please use a different email:"
                })
                return state
        
        # Save the field
        if current_field == "email":
            state["user_email"] = processed_value
        
        state["user_data"][current_field] = processed_value
        
        # Move to next field for create operation
        if state["current_intent"] == "create":
            next_field = self._get_next_field(current_field)
            
            if next_field:
                state["collecting_field"] = next_field
                field_name = self.REQUIRED_FIELDS[next_field]
                state["messages"].append({
                    "role": "assistant",
                    "content": f"✓ Got it! Now, what is your {field_name}?"
                })
            else:
                # All fields collected
                state["operation_complete"] = True
                state["collecting_field"] = None
        
        elif state["current_intent"] in ["read", "delete"]:
            state["operation_complete"] = True
        
        elif state["current_intent"] == "update":
            if current_field == "email":
                # Ask for field to update
                state["collecting_field"] = "update_field_name"
                fields_list = "\n".join([f"{i+1}. {v}" for i, v in enumerate(self.UPDATEABLE_FIELDS.values())])
                state["messages"].append({
                    "role": "assistant",
                    "content": f"Which field would you like to update?\n\n{fields_list}\n\nJust tell me the field name or number:"
                })
            elif current_field == "update_field_name":
                # Identify which field and ask for new value
                field_key = self._identify_update_field(processed_value)
                if field_key:
                    state["user_data"]["update_field_key"] = field_key
                    state["collecting_field"] = field_key
                    state["messages"].append({
                        "role": "assistant",
                        "content": f"What is the new value for {self.UPDATEABLE_FIELDS[field_key]}?"
                    })
                else:
                    state["messages"].append({
                        "role": "assistant",
                        "content": "I couldn't identify that field. Please specify which field you want to update:"
                    })
            else:
                # Got the new value
                state["operation_complete"] = True
        
        return state
    
    def _validate_field(self, field: str, value: str) -> tuple[bool, str, Any]:
        """Validate field value."""
        if field == "email":
            is_valid, error = validate_email(value)
            return is_valid, error or "", value.lower().strip() if is_valid else None
        
        elif field == "phone_number":
            is_valid, error, formatted = validate_phone(value)
            return is_valid, error or "", formatted
        
        elif field == "date_of_birth":
            is_valid, error, parsed_date = validate_date(value, "date_of_birth")
            return is_valid, error or "", parsed_date
        
        elif field == "full_name":
            if len(value.strip()) < 2:
                return False, "Name must be at least 2 characters", None
            return True, "", value.strip()
        
        elif field == "address":
            if len(value.strip()) < 5:
                return False, "Address must be at least 5 characters", None
            return True, "", value.strip()
        
        elif field in ["update_field", "update_field_name"]:
            return True, "", value.strip()
        
        return True, "", value.strip()
    
    def _get_next_field(self, current_field: str) -> str | None:
        """Get the next field to collect."""
        fields = list(self.REQUIRED_FIELDS.keys())
        try:
            current_idx = fields.index(current_field)
            if current_idx + 1 < len(fields):
                return fields[current_idx + 1]
        except ValueError:
            pass
        return None
    
    def _identify_update_field(self, user_input: str) -> str | None:
        """Identify which field user wants to update."""
        user_input_lower = user_input.lower().strip()
        
        # Check for number
        if user_input_lower.isdigit():
            idx = int(user_input_lower) - 1
            fields = list(self.UPDATEABLE_FIELDS.keys())
            if 0 <= idx < len(fields):
                return fields[idx]
        
        # Check for field name
        for key, display_name in self.UPDATEABLE_FIELDS.items():
            if key.replace("_", " ") in user_input_lower or display_name.lower() in user_input_lower:
                return key
        
        return None
    
    def execute_operation_node(self, state: ConversationState) -> ConversationState:
        """Execute the database operation."""
        intent = state["current_intent"]
        
        try:
            if intent == "create":
                result = self._execute_create(state)
            elif intent == "read":
                result = self._execute_read(state)
            elif intent == "update":
                result = self._execute_update(state)
            elif intent == "delete":
                result = self._execute_delete(state)
            else:
                result = "❌ Unknown operation"
            
            state["messages"].append({
                "role": "assistant",
                "content": result
            })
            
        except Exception as e:
            logger.error(f"Operation failed: {e}")
            state["messages"].append({
                "role": "assistant",
                "content": f"❌ An error occurred: {str(e)}"
            })
        
        return state
    
    def _execute_create(self, state: ConversationState) -> str:
        """Execute create operation."""
        data = state["user_data"]
        
        user = User(
            full_name=data["full_name"],
            email=data["email"],
            phone_number=data["phone_number"],
            date_of_birth=data["date_of_birth"],
            address=data["address"]
        )
        
        created_user = self.repository.create(user)
        
        return f"""✅ Registration created successfully!

📋 **Your Details:**
👤 Name: {created_user.full_name}
📧 Email: {created_user.email}
📱 Phone: {created_user.phone_number}
🎂 Date of Birth: {created_user.date_of_birth}
🏠 Address: {created_user.address}

Your registration ID is: {created_user.id}

What else can I help you with?"""
    
    def _execute_read(self, state: ConversationState) -> str:
        """Execute read operation."""
        email = state["user_email"]
        user = self.repository.get_by_email(email)
        
        if not user:
            return f"❌ No registration found for email: {email}"
        
        return f"""📋 **Your Registration Details:**

👤 Name: {user.full_name}
📧 Email: {user.email}
📱 Phone: {user.phone_number}
🎂 Date of Birth: {user.date_of_birth}
🏠 Address: {user.address}

📅 Registered: {user.created_at.strftime('%Y-%m-%d %H:%M')}
🔄 Last Updated: {user.updated_at.strftime('%Y-%m-%d %H:%M')}

What else can I help you with?"""
    
    def _execute_update(self, state: ConversationState) -> str:
        """Execute update operation."""
        email = state["user_email"]
        field_key = state["user_data"].get("update_field_key")
        new_value = state["user_data"].get(field_key)
        
        if not field_key or not new_value:
            return "❌ Update information is incomplete"
        
        # Create update object
        update_data = {field_key: new_value}
        update = UserUpdate(**update_data)
        
        updated_user = self.repository.update(email, update)
        
        if not updated_user:
            return f"❌ No registration found for email: {email}"
        
        field_display = self.UPDATEABLE_FIELDS[field_key]
        
        return f"""✅ Successfully updated {field_display}!

📋 **Updated Registration:**
👤 Name: {updated_user.full_name}
📧 Email: {updated_user.email}
📱 Phone: {updated_user.phone_number}
🎂 Date of Birth: {updated_user.date_of_birth}
🏠 Address: {updated_user.address}

What else can I help you with?"""
    
    def _execute_delete(self, state: ConversationState) -> str:
        """Execute delete operation."""
        email = state["user_email"]
        deleted = self.repository.delete(email)
        
        if deleted:
            return f"""✅ Registration for {email} has been successfully deleted.

All your data has been removed from our system.

If you need to register again, just let me know!"""
        else:
            return f"❌ No registration found for email: {email}"
    
    def chat(self, message: str, state: ConversationState | None = None) -> tuple[str, ConversationState]:
        """
        Process a user message and return response.
        
        Args:
            message: User message
            state: Current conversation state (or None for new conversation)
            
        Returns:
            Tuple of (response_message, updated_state)
        """
        if state is None:
            state = create_initial_state()
        
        # Add user message to state
        state["messages"].append({
            "role": "user",
            "content": message
        })
        
        # Run the graph with recursion limit
        result_state = self.graph.invoke(state, {"recursion_limit": 50})
        
        # Get assistant's response (last message)
        if result_state["messages"] and result_state["messages"][-1]["role"] == "assistant":
            response = result_state["messages"][-1]["content"]
        else:
            response = "I'm not sure how to help with that. Type 'help' to see what I can do."
        
        return response, result_state
