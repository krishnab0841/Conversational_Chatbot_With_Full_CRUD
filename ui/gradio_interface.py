"""
Gradio-based web interface for the chatbot.
"""

import logging
import gradio as gr
from typing import List, Tuple

from chatbot import ChatbotAgent
from chatbot.state import create_initial_state, ConversationState

logger = logging.getLogger(__name__)


class GradioInterface:
    """Gradio web interface for the chatbot."""
    
    def __init__(self):
        """Initialize Gradio interface."""
        self.agent = ChatbotAgent()
        self.conversation_states = {}  # Store states per session
        
        logger.info("Gradio interface initialized")
    
    def chat(self, message: str, history: List[List[str]], session_id: str) -> Tuple[List[List[str]], str]:
        """
        Handle chat interaction.
        
        Args:
            message: User message
            history: Chat history
            session_id: Session identifier
            
        Returns:
            Tuple of (updated_history, empty_input)
        """
        if not message.strip():
            return history, ""
        
        # Get or create state for this session
        if session_id not in self.conversation_states:
            self.conversation_states[session_id] = create_initial_state()
        
        state = self.conversation_states[session_id]
        
        try:
            # Process message through agent
            response, updated_state = self.agent.chat(message, state)
            
            # Update state
            self.conversation_states[session_id] = updated_state
            
            # Update history
            history.append([message, response])
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            response = f"❌ An error occurred: {str(e)}\n\nPlease try again."
            history.append([message, response])
        
        return history, ""
    
    def clear_chat(self, session_id: str):
        """Clear chat history and state."""
        if session_id in self.conversation_states:
            del self.conversation_states[session_id]
        return [], ""
    
    def launch(self, share: bool = False):
        """
        Launch the Gradio interface.
        
        Args:
            share: Whether to create a public share link
        """
        with gr.Blocks(
            title="AI Registration Assistant",
            theme=gr.themes.Soft(
                primary_hue="blue",
                secondary_hue="slate",
            ),
            css="""
                .chatbot-container {
                    height: 600px !important;
                }
                .input-container {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px;
                    border-radius: 10px;
                }
                #header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                    text-align: center;
                    margin-bottom: 20px;
                }
                .footer {
                    text-align: center;
                    padding: 20px;
                    color: #666;
                }
            """
        ) as interface:
            
            # Session state
            session_id = gr.State(value=lambda: str(id({})))
            
            # Header
            gr.HTML("""
                <div id="header">
                    <h1>🤖 AI Registration Assistant</h1>
                    <p style="font-size: 18px; margin: 10px 0 0 0;">
                        Conversational AI for Managing Your Registration Data
                    </p>
                </div>
            """)
            
            # Info section
            with gr.Accordion("ℹ️ What can I do?", open=False):
                gr.Markdown("""
                    I'm your intelligent registration assistant powered by Google Gemini and LangGraph! I can help you with:
                    
                    - 🆕 **Create** a new registration
                    - 📖 **Read** your existing registration details
                    - ✏️ **Update** specific fields in your registration
                    - 🗑️ **Delete** your registration
                    
                    Just chat with me naturally! For example:
                    - "I want to register"
                    - "Show me my details for john@example.com"
                    - "Update my phone number"
                    - "Delete my account"
                """)
            
            # Chatbot
            chatbot = gr.Chatbot(
                label="Chat",
                elem_classes="chatbot-container",
                height=600,
                show_label=False,
                avatar_images=(None, "https://api.dicebear.com/7.x/bottts/svg?seed=Assistant"),
            )
            
            # Input area
            with gr.Row(elem_classes="input-container"):
                with gr.Column(scale=9):
                    msg_input = gr.Textbox(
                        placeholder="Type your message here... (e.g., 'I want to create a new registration')",
                        show_label=False,
                        container=False,
                        scale=7
                    )
                with gr.Column(scale=1):
                    submit_btn = gr.Button("Send", variant="primary", scale=1)
            
            # Control buttons
            with gr.Row():
                clear_btn = gr.Button("🔄 Clear Chat", variant="secondary")
                example_btn1 = gr.Button("💡 Example: Create Registration", variant="secondary")
                example_btn2 = gr.Button("💡 Example: View My Data", variant="secondary")
            
            # Footer
            gr.HTML("""
                <div class="footer">
                    <p>Powered by <strong>LangGraph</strong> + <strong>Google Gemini</strong> + <strong>PostgreSQL</strong></p>
                    <p>All data is stored securely with full audit logging</p>
                </div>
            """)
            
            # Event handlers
            msg_input.submit(
                self.chat,
                inputs=[msg_input, chatbot, session_id],
                outputs=[chatbot, msg_input]
            )
            
            submit_btn.click(
                self.chat,
                inputs=[msg_input, chatbot, session_id],
                outputs=[chatbot, msg_input]
            )
            
            clear_btn.click(
                self.clear_chat,
                inputs=[session_id],
                outputs=[chatbot, msg_input]
            )
            
            example_btn1.click(
                lambda: "I want to create a new registration",
                outputs=[msg_input]
            )
            
            example_btn2.click(
                lambda: "Show me my registration details",
                outputs=[msg_input]
            )
        
        # Launch
        logger.info("Launching Gradio interface")
        interface.launch(
            share=share,
            server_name="0.0.0.0",
            server_port=7860,
            show_error=True
        )


def launch_web_interface(share: bool = False):
    """
    Launch the web interface.
    
    Args:
        share: Whether to create a public share link
    """
    interface = GradioInterface()
    interface.launch(share=share)
