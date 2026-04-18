# AI DevOps Assistant

AI-powered code generation and error fixing tool.

## Structure

```
ai-devops-assistant/
├── backend/
│   └── app/
│       ├── main.py              # FastAPI entry point
│       ├── routes/              # API endpoints
│       │   ├── generate.py      # Component generation
│       │   └── error_fix.py     # Error analysis
│       ├── services/            # Business logic
│       │   ├── ai_service.py    # AI operations
│       │   └── analyzer.py      # Error analysis
│       └── models/              # Data models
├── frontend/
│   └── src/
│       ├── components/          # Reusable UI
│       ├── pages/               # Route pages
│       │   ├── GeneratePage.jsx
│       │   └── ErrorFixPage.jsx
│       └── services/            # API calls
│           └── api.js
└── docs/                        # Documentation
```

## Backend (FastAPI)

### Routes
- `POST /generate/` - Generate React components
- `POST /fix-error/` - Analyze and fix code errors

### Services
- **ai_service.py**: Handles AI-powered code generation
- **analyzer.py**: Identifies affected files and dependencies

## Frontend (React + Vite)

### Pages
- **GeneratePage**: Component generation interface
- **ErrorFixPage**: Error analysis interface

### Services
- **api.js**: All HTTP requests to backend

## Running Locally

### Backend
```bash
cd backend
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm run dev
```

## SOLID Principles Applied

- **S**: Single Responsibility - Each module has one job
- **O**: Open/Closed - Services extendable without modification
- **L**: Liskov Substitution - Models can be substituted
- **I**: Interface Segregation - Routes only use what they need
- **D**: Dependency Inversion - Routes depend on service interfaces
