# Quick Start Guide

## 🚀 5-Minute Setup

### 1. Install Dependencies
```bash
cd d:\AI_Agent_Chatbot
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
copy .env.example .env
```

Edit `.env` and add:
- Your Google Gemini API key
- PostgreSQL password

### 3. Setup Database

**Create Database:**
Open PostgreSQL and run:
```sql
CREATE DATABASE chatbot_db;
```

**Initialize Schema:**
```bash
python main.py --init-db
```

### 4. Run the Chatbot

**Web Interface:**
```bash
python main.py --mode web
```
Then open http://localhost:7860

**CLI Interface:**
```bash
python main.py --mode cli
```

## 📝 Example Conversation

```
You: I want to register
Bot: I'll help you create a new registration. What is your full name?

You: John Doe
Bot: ✓ Got it! Now, what is your Email Address?

You: john@example.com
Bot: ✓ Got it! Now, what is your Phone Number?

You: +1234567890
Bot: ✓ Got it! Now, what is your Date of Birth (YYYY-MM-DD)?

You: 1990-01-15
Bot: ✓ Got it! Now, what is your Full Address?

You: 123 Main St, New York, NY 10001
Bot: ✅ Registration created successfully!
```

## 🎯 Common Commands

- **Create**: "I want to register", "create new account"
- **Read**: "Show my details", "view my registration"
- **Update**: "Update my phone", "change my address"
- **Delete**: "Delete my account", "remove my registration"
- **Help**: "help", "what can you do"

## 🔧 Troubleshooting

**Can't connect to database?**
```bash
python main.py --test-db
```

**Need to reset database?**
```bash
python main.py --init-db
```

**Want to see detailed logs?**
```bash
python main.py --mode web --log-level DEBUG
```

## 🎬 Run Demo
```bash
python demo/demo_script.py
```

This demonstrates all CRUD operations automatically!
