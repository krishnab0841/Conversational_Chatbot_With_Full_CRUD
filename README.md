# 🤖 AI Agent Chatbot

A conversational AI chatbot for CRUD operations on user registration data using natural language. Built with **LangGraph**, **Google Gemini**, **React**, **FastAPI**, and **PostgreSQL**.

---

## ✨ Features

- **💬 Natural Language Interface**: Powered by Google Gemini 2.0 Flash
- **🔄 Full CRUD Operations**: Create, Read, Update, Delete user registrations
- **🧠 Agentic AI**: LangGraph state machine for intelligent conversation flow
- **✅ Smart Validation**: Email, phone, date validation with user-friendly error messages
- **📊 Audit Logging**: Complete audit trail of all database operations
- **🎨 Modern UI**: Beautiful React frontend with real-time chat
- **🔒 Secure**: PostgreSQL with proper constraints and parameterized queries
- **📱 Responsive**: Works on desktop and mobile devices

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│              React Frontend (Port 5173)                  │
│        Modern UI with real-time chat interface           │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST
┌────────────────────▼────────────────────────────────────┐
│           FastAPI Backend (Port 8000)                    │
│              REST API with CORS support                  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                LangGraph Agent                           │
│   Intent Classification → Data Collection →             │
│   Validation → CRUD Execution → Response                │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│             PostgreSQL Database                          │
│        Users Table  │  Audit Log Table                  │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 Prerequisites

- **Python** 3.10 or higher
- **Node.js** 18+ and npm
- **PostgreSQL** 12 or higher
- **Google Gemini API** key ([Get one here](https://makersuite.google.com/app/apikey))

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/AI_Agent_Chatbot.git
cd AI_Agent_Chatbot
```

### 2. Backend Setup

**Create virtual environment:**
```bash
python -m venv venv
```

**Activate virtual environment:**
```bash
# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

### 3. Database Setup

**Create PostgreSQL database:**
```sql
-- Connect to PostgreSQL and run:
CREATE DATABASE chatbot_db;
```

**Configure environment:**
```bash
# Copy example file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

**Edit `.env` with your credentials:**
```env
# Google Gemini API
GOOGLE_API_KEY=your_google_api_key_here

# Database Configuration
DB_NAME=chatbot_db
DB_USER=postgres
DB_PASSWORD=your_postgresql_password
DB_HOST=localhost
DB_PORT=5432

# Application Settings
GEMINI_MODEL=gemini-2.0-flash-exp
LOG_LEVEL=INFO
```

**Initialize database schema:**
```bash
python main.py --init-db
```

**Test database connection:**
```bash
python main.py --test-db
```

### 4. Frontend Setup

**Navigate to frontend directory:**
```bash
cd frontend
```

**Install dependencies:**
```bash
npm install
```

---

## 🎯 Running the Application

You need **two terminal windows** - one for backend, one for frontend.

### Terminal 1 - Backend

**Run ONE of these commands (they do the same thing):**

```bash
# Option 1: Using main.py
python main.py

# Option 2: Using backend.py directly  
python backend.py
```

Backend runs on: **http://localhost:8000**

### Terminal 2 - Frontend

```bash
# From project root
cd frontend
npm run dev
```

Frontend runs on: **http://localhost:5173**

**Open your browser** to `http://localhost:5173` and start chatting! 🎉

---

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
     📞 Phone: +1234567890
     🎂 Date of Birth: 1990-01-15
     🏠 Address: 123 Main St, New York, NY 10001, USA
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
Bot: ✅ Registration deleted successfully!
```

---

## 📁 Project Structure

```
AI_Agent_Chatbot/
├── backend.py              # FastAPI REST API server
├── main.py                 # Entry point (runs backend)
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
├── .gitignore             # Git ignore rules
│
├── chatbot/               # LangGraph agent
│   ├── agent.py          # Main agent logic
│   ├── state.py          # Conversation state
│   └── tools.py          # CRUD tools
│
├── config/                # Configuration
│   ├── __init__.py
│   └── settings.py       # Pydantic settings
│
├── database/              # Database layer
│   ├── connection.py     # DB connection
│   ├── models.py         # Data models
│   ├── repository.py     # CRUD operations
│   └── schema.sql        # Database schema
│
├── utils/                 # Utilities
│   ├── logging_config.py # Logging setup
│   └── validators.py     # Input validation
│
├── demo/                  # Demo scripts
│   └── demo_script.py
│
└── frontend/              # React frontend
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── main.jsx       # React entry point
        ├── App.jsx        # Main app component
        ├── App.css        # Styling
        ├── components/    # React components
        │   ├── Header.jsx
        │   ├── ChatMessage.jsx
        │   └── ChatInput.jsx
        └── services/
            └── api.js     # Backend API client
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API status |  
| `GET` | `/api/health` | Health check |
| `POST` | `/api/chat` | Send message, get response |
| `POST` | `/api/clear` | Clear conversation history |

### Example API Request

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want to create a new registration",
    "session_id": "optional-session-id"
  }'
```

---

## 🗄️ Database Schema

### Users Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | SERIAL | Primary key |
| `full_name` | VARCHAR(255) | User's full name |
| `email` | VARCHAR(255) | Unique email (indexed) |
| `phone_number` | VARCHAR(20) | Phone in E164 format |
| `date_of_birth` | DATE | Date of birth |
| `address` | TEXT | Full address |
| `created_at` | TIMESTAMP | Registration time |
| `updated_at` | TIMESTAMP | Last update time |

### Audit Log Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | SERIAL | Primary key |
| `user_id` | INTEGER | Foreign key to users |
| `operation` | VARCHAR(50) | CREATE/READ/UPDATE/DELETE |
| `operation_details` | JSONB | Operation metadata |
| `performed_at` | TIMESTAMP | Operation timestamp |

---

## 🛠️ Development

### Backend Development

```bash
# Run with hot reload
uvicorn backend:app --reload --port 8000

# View logs
python main.py --log-level DEBUG
```

### Frontend Development

```bash
cd frontend

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Database Commands

```bash
# Initialize database
python main.py --init-db

# Test connection
python main.py --test-db

# View database logs
# Check logs/chatbot.log
```

---

## 🛡️ Security Features

- ✅ **Input Validation**: Pydantic models with strict validation
- ✅ **SQL Injection Prevention**: Parameterized queries
- ✅ **Email Validation**: RFC-compliant email checking
- ✅ **Phone Validation**: International phone number support
- ✅ **Date Validation**: Age constraints and format checking
- ✅ **CORS Protection**: Configured for specific origins
- ✅ **Audit Logging**: Complete operation trail
- ✅ **Error Handling**: User-friendly error messages

---

## 🐛 Troubleshooting

### Database Connection Issues

**Problem:** `Database connection failed`

**Solutions:**
- Verify PostgreSQL is running
- Check credentials in `.env`
- Ensure database `chatbot_db` exists
- Test with: `python main.py --test-db`

### API Key Errors

**Problem:** `Google API authentication error`

**Solutions:**
- Verify `GOOGLE_API_KEY` in `.env`
- Check key is active at [Google AI Studio](https://makersuite.google.com/)
- Ensure no extra spaces in key

### Module Import Errors

**Problem:** `ModuleNotFoundError`

**Solutions:**
- Activate virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`
- For frontend: `cd frontend && npm install`

### Frontend Connection Issues

**Problem:** Frontend can't connect to backend

**Solutions:**
- Ensure backend is running on port 8000
- Check browser console for CORS errors
- Verify API URL in `frontend/src/services/api.js`

### Port Already in Use

**Problem:** `Port 8000 already in use`

**Solutions:**
- Stop other instances of the backend
- Change port in `backend.py` (line 164-168)
- Kill process using the port

---

## 📦 Dependencies

### Backend

- `langgraph` - Agentic AI framework
- `langchain` - LLM orchestration
- `langchain-google-genai` - Google Gemini integration
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `psycopg2-binary` - PostgreSQL driver
- `sqlalchemy` - ORM
- `pydantic` - Data validation
- `python-dotenv` - Environment management
- `colorlog` - Colored logging

### Frontend

- `react` - UI library
- `vite` - Build tool
- `axios` - HTTP client

---

## 🔄 CI/CD & Deployment

### Build for Production

**Backend:**
```bash
pip install -r requirements.txt
python main.py --init-db
```

**Frontend:**
```bash
cd frontend
npm run build
# Output in frontend/dist/
```

### Docker Support

Coming soon! 🐳

---

## 📝 License

This project is created for educational and demonstration purposes.

---

## 🙏 Acknowledgments

- **LangGraph** - Agentic AI framework
- **Google Gemini** - Language model API
- **React** - Frontend framework
- **FastAPI** - Backend framework
- **PostgreSQL** - Database system
- **Vite** - Build tool

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

---

## 📧 Support

For issues or questions:
- Check `logs/chatbot.log` for detailed logs
- Run with `--log-level DEBUG` for more info
- Open an issue on GitHub

---

**Built with ❤️ using LangGraph + Google Gemini + React + FastAPI + PostgreSQL**
