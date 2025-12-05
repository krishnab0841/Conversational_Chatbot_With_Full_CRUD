"""
Main entry point for the AI Agent Chatbot.
Handles initialization and launches the appropriate interface.
"""

import sys
import argparse
import logging

from config import get_settings
from utils import setup_logging
from database import init_database, test_connection
from ui import launch_web_interface, launch_cli_interface

logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="AI Agent Chatbot - Conversational CRUD Operations with PostgreSQL"
    )
    
    parser.add_argument(
        "--mode",
        choices=["web", "cli"],
        default=None,
        help="Interface mode: web (Gradio) or cli (command-line). Defaults to value in .env"
    )
    
    parser.add_argument(
        "--init-db",
        action="store_true",
        help="Initialize database with schema"
    )
    
    parser.add_argument(
        "--test-db",
        action="store_true",
        help="Test database connection"
    )
    
    parser.add_argument(
        "--share",
        action="store_true",
        help="Create public share link (Gradio web mode only)"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default=None,
        help="Logging level. Defaults to value in .env"
    )
    
    return parser.parse_args()


def main():
    """Main application entry point."""
    args = parse_args()
    
    try:
        # Load settings
        settings = get_settings()
        
        # Setup logging
        log_level = args.log_level or settings.log_level
        setup_logging(log_level)
        
        logger.info("Starting AI Agent Chatbot")
        logger.info(f"Using model: {settings.gemini_model}")
        
        # Handle database initialization
        if args.init_db:
            print("\n🔧 Initializing database...")
            init_database()
            print("✅ Database initialized successfully!\n")
            return 0
        
        # Handle database test
        if args.test_db:
            print("\n🔍 Testing database connection...")
            if test_connection():
                print("✅ Database connection successful!\n")
                return 0
            else:
                print("❌ Database connection failed. Check your configuration.\n")
                return 1
        
        # Test database connection before starting
        if not test_connection():
            print("\n❌ Failed to connect to database!")
            print("Please check your database configuration in .env")
            print("\nYou can:")
            print("  1. Run 'python main.py --init-db' to initialize the database")
            print("  2. Run 'python main.py --test-db' to test the connection\n")
            return 1
        
        print("\n✅ Database connection successful!")
        
        # Determine mode
        mode = args.mode or settings.app_mode
        
        # Launch appropriate interface
        if mode == "web":
            logger.info("Launching web interface")
            print("\n🚀 Launching Gradio web interface...")
            print("The interface will open in your browser shortly.\n")
            launch_web_interface(share=args.share)
        
        elif mode == "cli":
            logger.info("Launching CLI interface")
            launch_cli_interface()
        
        else:
            print(f"\n❌ Invalid mode: {mode}")
            print("Please set APP_MODE in .env to 'web' or 'cli'\n")
            return 1
        
        return 0
        
    except FileNotFoundError as e:
        print(f"\n❌ Configuration error: {e}")
        print("\nPlease create a .env file based on .env.example")
        print("and configure your settings.\n")
        return 1
    
    except Exception as e:
        logger.exception("Application error")
        print(f"\n❌ An error occurred: {str(e)}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
