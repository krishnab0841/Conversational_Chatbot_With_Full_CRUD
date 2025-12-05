# AI Agent Chatbot - CRUD Operations with PostgreSQL

A conversational AI chatbot that enables users to perform full CRUD (Create, Read, Update, Delete) operations on registration data using natural language. Built with LangGraph for agentic flow management, Google Gemini for AI capabilities, and PostgreSQL for data persistence.

## ✨ Features

- **🤖 Conversational AI**: Natural language interface powered by Google Gemini
- **🔄 Full CRUD Operations**: Create, Read, Update, and Delete user registrations
- **🧠 Agentic Flow**: LangGraph-based state machine for intelligent conversation management
- **✅ Smart Validation**: Comprehensive input validation for emails, phone numbers, and dates
- **📊 Audit Logging**: Complete audit trail of all database operations
- **🎨 Dual Interface**: Beautiful Gradio web UI and CLI option
- **🔒 Data Security**: PostgreSQL with proper constraints and validation

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   User Interfaces                        │
│         Gradio Web UI  │  Command Line                  │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│               LangGraph Agent                            │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Intent Classification → Data Collection        │   │
│  │  → Validation → CRUD Execution → Response       │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│              PostgreSQL Database                         │
│         Users Table  │  Audit Log Table                 │
└─────────────────────────────────────────────────────────┘
```

## 📋 Prerequisites

- Python 3.10 or higher
- PostgreSQL 12 or higher
- Google Gemini API key

## 🚀 Quick Start

### 1. Clone and Setup

```bash
cd d:\AI_Agent_Chatbot
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file from the example:

```bash
copy .env.example .env
```

Edit `.env` with your credentials:

```env
GOOGLE_API_KEY=your_google_api_key_here
DB_PASSWORD=your_postgresql_password
DB_NAME=chatbot_db
DB_USER=postgres
DB_HOST=localhost
DB_PORT=5432
APP_MODE=web
```

### 3. Setup Database

First, create the PostgreSQL database:

```sql
-- Connect to PostgreSQL and run:
CREATE DATABASE chatbot_db;
```

Then initialize the schema:

```bash
python main.py --init-db
```

### 4. Test Connection

```bash
python main.py --test-db
```

### 5. Run the Application

**Web Interface (Gradio):**
```bash
python main.py --mode web
```

**CLI Interface:**
```bash
python main.py --mode cli
```

**Public Share Link:**
```bash
python main.py --mode web --share
```

## 📖 Usage Examples

### Creating a Registration

```
You: I want to create a new registration
Bot: I'll help you create a new registration. Let's start! What is your full name?
You: John Doe
Bot: ✓ Got it! Now, what is your Email Address?
You: john.doe@example.com
Bot: ✓ Got it! Now, what is your Phone Number?
You: +1234567890
Bot: ✓ Got it! Now, what is your Date of Birth (YYYY-MM-DD)?
You: 1990-01-15
Bot: ✓ Got it! Now, what is your Full Address?
You: 123 Main St, New York, NY 10001, USA
Bot: ✅ Registration created successfully!
```

### Reading Registration

```
You: Show me my registration for john.doe@example.com
Bot: 📋 Your Registration Details:
     👤 Name: John Doe
     📧 Email: john.doe@example.com
     ...
```

### Updating Registration

```
You: I need to update my phone number
Bot: I'll help you update your registration. First, what is your email address?
You: john.doe@example.com
Bot: Which field would you like to update?
You: phone number
Bot: What is the new value for Phone Number?
You: +9876543210
Bot: ✅ Successfully updated Phone Number!
```

### Deleting Registration

```
You: Delete my registration
Bot: I'll help you delete your registration. What is your email address?
You: john.doe@example.com
Bot: ✅ Registration for john.doe@example.com has been successfully deleted.
```

## 📁 Project Structure

```
AI_Agent_Chatbot/
├── chatbot/                 # LangGraph agent implementation
│   ├── agent.py            # Main agent with conversation flow
│   └── state.py            # Conversation state management
├── config/                  # Configuration management
│   └── settings.py         # Settings with Pydantic
├── database/               # Database layer
│   ├── connection.py       # DB connection handling
│   ├── models.py           # Pydantic models
│   ├── repository.py       # CRUD operations
│   └── schema.sql          # Database schema
├── ui/                     # User interfaces
│   ├── gradio_interface.py # Web UI
│   └── cli_interface.py    # Command-line UI
├── utils/                  # Utilities
│   ├── logging_config.py   # Logging setup
│   └── validators.py       # Input validation
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
└── README.md              # This file
```

## 🗄️ Database Schema

**Users Table:**
- `id`: Primary key
- `full_name`: User's full name
- `email`: Unique email address
- `phone_number`: Phone in E164 format
- `date_of_birth`: Date of birth
- `address`: Full address
- `created_at`: Registration timestamp
- `updated_at`: Last update timestamp

**Audit Log Table:**
- `id`: Primary key
- `user_id`: Reference to user
- `operation`: CREATE/READ/UPDATE/DELETE
- `operation_details`: JSON metadata
- `performed_at`: Operation timestamp

## 🔧 Configuration Options

### Command Line Arguments

- `--mode [web|cli]`: Interface mode
- `--init-db`: Initialize database schema
- `--test-db`: Test database connection
- `--share`: Create public Gradio link
- `--log-level [DEBUG|INFO|WARNING|ERROR]`: Set logging level

### Environment Variables

See `.env.example` for all available configuration options.

## 🧪 Testing

Test database connection:
```bash
python main.py --test-db
```

View logs:
```bash
type logs\chatbot.log  # Windows
cat logs/chatbot.log   # Unix
```

## 🛡️ Security Features

- ✅ Input validation with Pydantic
- ✅ SQL injection prevention with parameterized queries
- ✅ Email format validation
- ✅ Phone number validation with international support
- ✅ Date validation with age constraints
- ✅ Database constraints and triggers
- ✅ Complete audit logging

## 🎨 UI Features

**Gradio Web Interface:**
- Modern gradient design
- Responsive chat interface
- Example prompts
- Session management
- Error handling with user-friendly messages

**CLI Interface:**
- Clean terminal UI
- Colored output
- Conversation flow
- Keyboard interrupt handling

## 📝 Development

### Adding New Features

1. **New CRUD Operation**: Add method to `UserRepository`
2. **New Validation**: Add validator to `utils/validators.py`
3. **New Intent**: Add node to LangGraph in `chatbot/agent.py`
4. **UI Enhancement**: Modify `ui/gradio_interface.py`

### Logging

Logs are written to:
- Console: Colored output
- File: `logs/chatbot.log`

## 🐛 Troubleshooting

**Database Connection Failed:**
- Check PostgreSQL is running
- Verify credentials in `.env`
- Ensure database exists

**API Key Error:**
- Verify `GOOGLE_API_KEY` in `.env`
- Check API key is active

**Module Import Errors:**
- Activate virtual environment
- Reinstall: `pip install -r requirements.txt`

## 📄 License

This project is created for educational and demonstration purposes.

## 🙏 Acknowledgments

- **LangGraph**: Agentic AI framework
- **Google Gemini**: Language model
- **Gradio**: Web interface framework
- **PostgreSQL**: Database system

## 📧 Support

For issues or questions, check the logs in `logs/chatbot.log` or run with `--log-level DEBUG`.

---

**Built with ❤️ using LangGraph + Google Gemini + PostgreSQL**
