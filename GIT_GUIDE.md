# Git Commands Reference

## Clone the Repository

```bash
git clone https://github.com/krishnab0841/Conversational_Chatbot_With_Full_CRUD.git
cd Conversational_Chatbot_With_Full_CRUD
```

## Setup After Cloning

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env with your credentials

# Initialize database
python main.py --init-db

# Run the application
python main.py --mode web
```

## Update Your Local Repository

```bash
# Pull latest changes
git pull origin main

# Check status
git status

# View commit history
git log --oneline
```

## Making Changes

```bash
# Create a new branch for your feature
git checkout -b feature/your-feature-name

# Make your changes, then...
git add .
git commit -m "Description of your changes"

# Push to GitHub
git push origin feature/your-feature-name
```

## Useful Git Commands

```bash
# View remote repository
git remote -v

# Check current branch
git branch

# Switch branches
git checkout main

# Discard local changes
git checkout -- .

# View differences
git diff
```
