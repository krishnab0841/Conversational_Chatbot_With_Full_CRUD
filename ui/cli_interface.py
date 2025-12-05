"""
Command-line interface for the chatbot.
"""

import logging
from typing import Optional

from chatbot import ChatbotAgent
from chatbot.state import create_initial_state, ConversationState

logger = logging.getLogger(__name__)


class CLIInterface:
    """Command-line interface for the chatbot."""
    
    def __init__(self):
        """Initialize CLI interface."""
        self.agent = ChatbotAgent()
        self.state: Optional[ConversationState] = None
        
        logger.info("CLI interface initialized")
    
    def print_welcome(self):
        """Print welcome message."""
        print("\n" + "="*70)
        print("🤖  AI REGISTRATION ASSISTANT".center(70))
        print("="*70)
        print("\nWelcome! I can help you manage your registration data.")
        print("\nType 'help' to see what I can do, or 'exit' to quit.\n")
    
    def run(self):
        """Run the CLI interface."""
        self.print_welcome()
        self.state = create_initial_state()
        
        while True:
            try:
                # Get user input
                user_input = input("\n💬 You: ").strip()
                
                if not user_input:
                    continue
                
                # Check for exit
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("\n👋 Thank you for using AI Registration Assistant. Goodbye!\n")
                    break
                
                # Process through agent
                response, self.state = self.agent.chat(user_input, self.state)
                
                # Display response
                print(f"\n🤖 Assistant: {response}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!\n")
                break
            
            except Exception as e:
                logger.error(f"CLI error: {e}")
                print(f"\n❌ An error occurred: {str(e)}")
                print("Please try again.\n")


def launch_cli_interface():
    """Launch the CLI interface."""
    cli = CLIInterface()
    cli.run()
