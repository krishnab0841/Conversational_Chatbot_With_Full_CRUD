"""
Demo script to showcase chatbot capabilities.
This script demonstrates all CRUD operations in sequence.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatbot import ChatbotAgent
from chatbot.state import create_initial_state
import time


def print_separator():
    """Print a visual separator."""
    print("\n" + "="*70 + "\n")


def demo_conversation(agent: ChatbotAgent):
    """Run a demonstration conversation."""
    print("\n" + "="*70)
    print("🤖  AI CHATBOT DEMO - CRUD OPERATIONS".center(70))
    print("="*70)
    
    state = create_initial_state()
    
    conversations = [
        # Help
        ("help", "Getting available commands"),
        
        # Create
        ("I want to create a new registration", "Starting registration"),
        ("Alice Johnson", "Providing name"),
        ("alice.johnson@example.com", "Providing email"),
        ("+14155551234", "Providing phone"),
        ("1995-03-20", "Providing date of birth"),
        ("456 Oak Avenue, San Francisco, CA 94102, USA", "Providing address"),
        
        # Read
        ("Show me my registration for alice.johnson@example.com", "Reading registration"),
        
        # Update
        ("I want to update my information", "Starting update"),
        ("alice.johnson@example.com", "Providing email for update"),
        ("phone number", "Selecting field to update"),
        ("+14155559999", "Providing new phone"),
        
        # Read again to verify update
        ("Show my details for alice.johnson@example.com", "Verifying update"),
        
        # Delete
        ("Delete my registration", "Starting deletion"),
        ("alice.johnson@example.com", "Confirming deletion"),
    ]
    
    for i, (message, description) in enumerate(conversations, 1):
        print_separator()
        print(f"Step {i}: {description}")
        print(f"\n💬 User: {message}")
        
        # Small delay for readability
        time.sleep(0.5)
        
        # Get response
        response, state = agent.chat(message, state)
        
        print(f"\n🤖 Assistant:\n{response}")
        
        # Pause between steps
        time.sleep(1)
    
    print_separator()
    print("✅ Demo completed successfully!")
    print("="*70 + "\n")


def main():
    """Run the demo."""
    print("\n🚀 Starting AI Chatbot Demo...\n")
    print("This will demonstrate:")
    print("  1. Help command")
    print("  2. Creating a new registration")
    print("  3. Reading registration data")
    print("  4. Updating a field")
    print("  5. Deleting registration")
    print("\nNote: This requires database connection to be configured.\n")
    
    input("Press Enter to continue...")
    
    try:
        agent = ChatbotAgent()
        demo_conversation(agent)
        
        print("\n💡 To run the actual chatbot:")
        print("   Web UI:  python main.py --mode web")
        print("   CLI:     python main.py --mode cli\n")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")
        print("\nMake sure:")
        print("  1. Database is configured (.env file)")
        print("  2. Database is initialized (python main.py --init-db)")
        print("  3. Dependencies are installed (pip install -r requirements.txt)\n")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
